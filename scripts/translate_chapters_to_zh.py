#!/usr/bin/env python3
"""Translate English chapter HTML into Chinese chapter HTML.

The script keeps page structure, attributes, code blocks, SVG, and scripts intact,
then asks the configured Anthropic-compatible model to translate prose-heavy HTML
chunks. It writes zh/chapters/chNN.html pages that use the shared app.js runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterable

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".translation-cache"

ZH_META = {
    1: ("第 1 章：环境搭建与分词", "从开发环境、Unicode 到 BPE 与 tokenizer 接口契约"),
    2: ("第 2 章：Embedding 层与位置编码", "TokenEmbedding、词向量、上下文化表示、RoPE 与长上下文"),
    3: ("第 3 章：单头自注意力", "Scaled Dot-Product Attention、mask、softmax 与诊断边界"),
    4: ("第 4 章：多头注意力与 MLA", "MHA、MQA、GQA、MLA 与 KV Cache 预算"),
    5: ("第 5 章：Transformer Block", "RMSNorm、SwiGLU、残差路径、稳定性与可解释性"),
    6: ("第 6 章：组装完整 GPT 模型", "GPT-2 124M、MoE、权重加载与 checkpoint 兼容性"),
    7: ("第 7 章：训练循环", "数据流水线、AdamW、checkpoint、分布式训练与工业诊断"),
    8: ("第 8 章：文本生成", "采样、beam、thinking budget、speculative decoding 与结构化输出"),
    9: ("第 9 章：微调与对齐", "SFT、LoRA、DPO、GRPO、RLVR 与 agentic RL"),
    10: ("第 10 章：推理优化与前沿", "KV Cache、attention 优化、serving、RAG 与多模态推理"),
    11: ("第 11 章：经典神经 NLP 与评估", "RNN、Parsing、Seq2Seq、BERT、评估协议与安全"),
}


PROMPT = """你在翻译一门大语言模型深度学习课程的 HTML 片段。

请严格按这些规则处理：
- 返回 HTML 片段本身，不要 Markdown 代码块，不要解释。
- 保留所有 HTML 标签、层级、id、class、href、src、onclick、data-answer、name、value 等属性。
- 不要删行、删表格、删列表项、删练习、删解释，也不要总结压缩。信息量必须和英文一致。
- 把面向学生阅读的英文正文翻译成自然中文，专业术语可以保留英文或中英混排，例如 token、logprob、KV Cache、rollout、SFT、DPO、GRPO。
- 代码、命令、变量名、函数名、文件路径、公式、占位符必须原样保留。
- data-explain、alt、aria-label、title 里如果是给用户读的说明，也翻译成中文；技术字段和代码不要翻译。
- 语言要像课程讲义，不要宣传腔，不要“综上所述”“本质上”这类空话。

HTML 片段如下：
"""


PROTECTED_RE = re.compile(
    r"(<pre[\s\S]*?</pre>|<script[\s\S]*?</script>|<style[\s\S]*?</style>|<svg[\s\S]*?</svg>|<code[\s\S]*?</code>)",
    re.IGNORECASE,
)


def protect_blocks(chunk: str) -> tuple[str, dict[str, str]]:
    protected: dict[str, str] = {}

    def repl(match: re.Match[str]) -> str:
        key = f"__PROTECTED_HTML_{len(protected)}__"
        protected[key] = match.group(0)
        return key

    return PROTECTED_RE.sub(repl, chunk), protected


def restore_blocks(chunk: str, protected: dict[str, str]) -> str:
    for key, value in protected.items():
        chunk = chunk.replace(key, value)
    return chunk


def split_main(main: str) -> list[str]:
    matches = list(re.finditer(r'<section class="card"(?:\s+id="[^"]+")?>[\s\S]*?</section>', main))
    if not matches:
        return [main]
    chunks: list[str] = []
    cursor = 0
    for match in matches:
        if match.start() > cursor:
            chunks.append(main[cursor : match.start()])
        chunks.append(match.group(0))
        cursor = match.end()
    if cursor < len(main):
        chunks.append(main[cursor:])
    return [chunk for chunk in chunks if chunk.strip()]


def cache_key(model: str, text: str) -> Path:
    digest = hashlib.sha256((model + "\n" + text).encode("utf-8")).hexdigest()
    return CACHE_DIR / f"{digest}.html"


def strip_fence(text: str) -> str:
    text = text.strip()
    fence = re.match(r"^```(?:html)?\s*([\s\S]*?)\s*```$", text)
    if fence:
        return fence.group(1).strip()
    return text


def translate_chunk(chunk: str, model: str, dry_run: bool = False) -> str:
    protected_chunk, protected = protect_blocks(chunk)
    if dry_run:
        return restore_blocks(protected_chunk, protected)

    CACHE_DIR.mkdir(exist_ok=True)
    path = cache_key(model, protected_chunk)
    if path.exists():
        return restore_blocks(path.read_text(encoding="utf-8"), protected)

    url = os.environ.get("ANTHROPIC_BASE_URL", "").rstrip("/") + "/v1/messages"
    token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not url.startswith("http") or not token:
        raise RuntimeError("ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN must be set")

    payload = {
        "model": model,
        "max_tokens": 16000,
        "messages": [{"role": "user", "content": PROMPT + protected_chunk}],
    }
    headers = {
        "x-api-key": token,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=240,
                proxies={"http": None, "https": None},
            )
            if response.status_code >= 400:
                raise RuntimeError(f"HTTP {response.status_code}: {response.text[:500]}")
            data = response.json()
            parts = [item.get("text", "") for item in data.get("content", []) if item.get("type") == "text"]
            translated = strip_fence("".join(parts))
            if not translated:
                raise RuntimeError("empty translation")
            path.write_text(translated, encoding="utf-8")
            return restore_blocks(translated, protected)
        except Exception as exc:  # pragma: no cover - operational retry
            last_error = exc
            time.sleep(2 + attempt * 3)
    raise RuntimeError(f"translation failed: {last_error}")


def rewrite_paths(markup: str, chapter: int) -> str:
    replacements = {
        'href="../images/': 'href="../../images/',
        'src="../images/': 'src="../../images/',
        'href="../css/': 'href="../../css/',
        'src="../js/': 'src="../../js/',
        'href="../assignments/': 'href="../../assignments/',
        'href="../docs/': 'href="../../docs/',
        'href="../en.html"': f'href="../../chapters/ch{chapter:02d}.html"',
        'href="ch': 'href="ch',
        'onclick="LLM.markComplete()"': 'onclick="LLM.markComplete()"',
    }
    for old, new in replacements.items():
        markup = markup.replace(old, new)
    markup = markup.replace("← Previous Chapter", "← 上一章")
    markup = markup.replace("Next Chapter →", "下一章 →")
    markup = markup.replace("✓ Mark Complete", "✓ 标记完成")
    markup = markup.replace("Check Answer", "检查答案")
    markup = markup.replace("Hint", "提示")
    markup = markup.replace("Font Size:", "字号：")
    markup = re.sub(r'LLM\.show[^("]*\(this\)', 'LLM.showHint(this)', markup)
    markup = re.sub(r"LLM\.check[^(]*\(this,'q([0-9]+)'\)", r"LLM.checkMC(this,'q\1')", markup)
    markup = re.sub(r"LLM\.set[^(]*\('([^']+)'\)", r"LLM.setFontSize('\1')", markup)
    markup = re.sub(r"LLM\.mark[^(]*\(\)", "LLM.markComplete()", markup)
    return markup


def extract_main(source: str) -> str:
    match = re.search(r'<main class="main">[\s\S]*?</main>', source)
    if not match:
        raise RuntimeError("cannot find <main class=\"main\">")
    return match.group(0)


def page_shell(chapter: int, main: str) -> str:
    title, subtitle = ZH_META[chapter]
    prev_link = f'<a href="ch{chapter - 1:02d}.html" class="btn btn-outline" rel="prev">← 上一章</a>' if chapter > 1 else ""
    next_link = f'<a href="ch{chapter + 1:02d}.html" class="btn btn-outline" rel="next">下一章 →</a>' if chapter < 11 else ""
    complete = '<button class="btn btn-primary" id="mark-complete" onclick="LLM.markComplete()">✓ 标记完成</button>'
    nav = f'\n<nav class="chapter-nav">\n  {prev_link}\n  {complete}\n  {next_link}\n</nav>\n'
    main = re.sub(r'<nav class="chapter-nav">[\s\S]*?</nav>', nav.strip(), main)
    main = rewrite_paths(main, chapter)
    title_attr = html.escape(f"{title} - LLM Deep Learning 中文版")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
  <link rel="icon" type="image/svg+xml" href="../../images/favicon.svg">
  <link rel="icon" type="image/x-icon" href="../../images/favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="../../images/favicon.png">
  <link rel="apple-touch-icon" href="../../images/favicon.png">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title_attr}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<link rel="stylesheet" href="../../css/style.css">
</head>
<body data-ch="{chapter}">

<button class="menu-toggle" aria-label="菜单">☰</button>
<aside class="sidebar" id="sidebar">
  <div class="sidebar-header"><h1>LLM Deep Learning</h1><p>中文版 · 从代码构建大语言模型</p></div>
  <nav class="sidebar-nav" id="sidebar-nav"></nav>
  <div class="sidebar-footer"><button class="theme-toggle" onclick="LLM.toggleTheme()"><span id="theme-icon">🌙</span> <span id="theme-label">深色模式</span></button></div>
</aside>

{main}

<button class="back-to-top" id="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="../../js/app.js"></script>
</body>
</html>
"""


def translate_chapter(chapter: int, model: str, dry_run: bool = False) -> None:
    source_path = ROOT / "chapters" / f"ch{chapter:02d}.html"
    output_path = ROOT / "zh" / "chapters" / f"ch{chapter:02d}.html"
    source = source_path.read_text(encoding="utf-8")
    main = extract_main(source)
    translated_chunks: list[str] = []
    chunks = split_main(main)
    print(f"ch{chapter:02d}: translating {len(chunks)} chunks", flush=True)
    for index, chunk in enumerate(chunks, 1):
        if not chunk.strip():
            translated_chunks.append(chunk)
            continue
        print(f"  chunk {index}/{len(chunks)} ({len(chunk)} chars)", flush=True)
        translated_chunks.append(translate_chunk(chunk, model, dry_run=dry_run))
    page = page_shell(chapter, "".join(translated_chunks))
    output_path.write_text(page, encoding="utf-8")
    print(f"ch{chapter:02d}: wrote {output_path}", flush=True)


def parse_chapters(values: Iterable[str]) -> list[int]:
    chapters: list[int] = []
    for value in values:
        if "-" in value:
            start, end = value.split("-", 1)
            chapters.extend(range(int(start), int(end) + 1))
        else:
            chapters.append(int(value))
    return sorted(set(chapters))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("chapters", nargs="*", help="chapter numbers or ranges, e.g. 7 8 9-11")
    parser.add_argument("--model", default=os.environ.get("ANTHROPIC_DEFAULT_HAIKU_MODEL", "deepseek-v4-flash"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    chapters = parse_chapters(args.chapters or ["1-11"])
    for chapter in chapters:
        if chapter not in ZH_META:
            raise SystemExit(f"unknown chapter: {chapter}")
        translate_chapter(chapter, args.model, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
