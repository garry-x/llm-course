#!/usr/bin/env python3
"""Polish Chinese course chapter HTML in-place.

The script keeps the English chapter structure intact while making the Chinese
prose less translation-like. It protects code, SVG, scripts, styles and inline
code, then sends section-sized HTML fragments to the configured
Anthropic-compatible endpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterable

import requests


ROOT = Path(__file__).resolve().parents[1]
CACHE_DIR = ROOT / ".polish-cache"

PROMPT = """你在润色一门大语言模型课程的中文 HTML 片段。场景是技术课程文档，不是营销文案，也不是聊天回复。

请严格遵守：
- 只返回润色后的 HTML 片段，不要 Markdown 代码块，不要解释。
- 保留所有 HTML 标签、层级、id、class、href、src、onclick、data-answer、name、value 等属性；不要增删 section、表格行、列表项、练习题、按钮、图片或链接。
- 保留代码、命令、变量名、函数名、字段名、文件路径、公式、指标名、模型名和英文技术术语；不要翻译或改写这些 protected spans。
- 不删信息点，不压缩内容，不把多段合并成短摘要。每个事实、条件、判断、数字、例子都要留在原位置附近。
- 目标是“说人话”：减少翻译腔和 AI 腔，改掉“本质上、值得注意的是、不仅仅是……更是……、不是……而是……、通过……来……、基于……”这类绕口或空泛表达。
- 句子要像课程讲义：直接、清楚、专业，但不要宣传腔、口号腔、过度拔高、空总结。
- 可以保留必要的英文术语和中英混排，例如 token、logprob、KV Cache、rollout、SFT、DPO、GRPO。
- 如果一句已经自然，不要为了改而改。

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
    return fence.group(1).strip() if fence else text


def polish_chunk(chunk: str, model: str, dry_run: bool = False) -> str:
    protected_chunk, protected = protect_blocks(chunk)
    visible_text = re.sub(r'<[^>]+>', ' ', protected_chunk)
    visible_text = re.sub(r'\s+', ' ', visible_text).strip()
    zh_chars = sum(1 for char in visible_text if '\u4e00' <= char <= '\u9fff')
    if zh_chars < 12:
        return chunk
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
            polished = strip_fence("".join(parts))
            if not polished:
                raise RuntimeError("empty polish result")
            polished = repair_runtime_names(polished)
            path.write_text(polished, encoding="utf-8")
            return restore_blocks(polished, protected)
        except Exception as exc:  # pragma: no cover - operational retry
            last_error = exc
            time.sleep(2 + attempt * 3)
    raise RuntimeError(f"polish failed: {last_error}")


def repair_runtime_names(markup: str) -> str:
    markup = re.sub(r'LLM\.show[^("]*\(this\)', 'LLM.showHint(this)', markup)
    markup = re.sub(r"LLM\.check[^(]*\(this,'q([0-9]+)'\)", r"LLM.checkMC(this,'q\1')", markup)
    markup = re.sub(r"LLM\.set[^(]*\('([^']+)'\)", r"LLM.setFontSize('\1')", markup)
    markup = re.sub(r"LLM\.mark[^(]*\(\)", "LLM.markComplete()", markup)
    return markup


def extract_main(source: str) -> tuple[str, str, str]:
    match = re.search(r'(<main class="main">[\s\S]*?</main>)', source)
    if not match:
        raise RuntimeError("cannot find <main class=\"main\">")
    return source[: match.start()], match.group(1), source[match.end() :]


def polish_chapter(chapter: int, model: str, dry_run: bool = False) -> None:
    path = ROOT / "zh" / "chapters" / f"ch{chapter:02d}.html"
    source = path.read_text(encoding="utf-8")
    prefix, main, suffix = extract_main(source)
    chunks = split_main(main)
    polished_chunks: list[str] = []
    print(f"ch{chapter:02d}: polishing {len(chunks)} chunks", flush=True)
    for index, chunk in enumerate(chunks, 1):
        print(f"  chunk {index}/{len(chunks)} ({len(chunk)} chars)", flush=True)
        polished_chunks.append(polish_chunk(chunk, model, dry_run=dry_run))
    path.write_text(prefix + "".join(polished_chunks) + suffix, encoding="utf-8")
    print(f"ch{chapter:02d}: wrote {path}", flush=True)


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
    parser.add_argument("chapters", nargs="*", help="chapter numbers or ranges, e.g. 1 2 7-11")
    parser.add_argument("--model", default=os.environ.get("ANTHROPIC_DEFAULT_HAIKU_MODEL", "deepseek-v4-flash"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for chapter in parse_chapters(args.chapters or ["1-11"]):
        if chapter < 1 or chapter > 11:
            raise SystemExit(f"unknown chapter: {chapter}")
        polish_chapter(chapter, args.model, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
