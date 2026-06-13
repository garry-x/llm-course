#!/usr/bin/env python3
"""Render course Markdown handouts into styled static HTML pages."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    "classic-nlp-deep-dive-module.md",
    "classic-nlp-handout.md",
    "math-prerequisites.md",
    "ml-foundations-prerequisite-bridge.md",
    "python-pytorch-review-session.md",
    "reading-list.md",
    "worked-example-pack.md",
    "written-problem-set.md",
]


def slugify(text: str, used: set[str]) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.lower(), flags=re.UNICODE).strip("-")
    slug = slug or "section"
    base = slug
    index = 2
    while slug in used:
        slug = f"{base}-{index}"
        index += 1
    used.add(slug)
    return slug


def rewrite_href(href: str, current_dir_prefix: str = "") -> str:
    if re.match(r"^(https?:|mailto:|#)", href):
        return href
    if ".md" in href:
        path, anchor = href.split("#", 1) if "#" in href else (href, "")
        path = re.sub(r"\.md$", ".html", path)
        href = f"{path}#{anchor}" if anchor else path
    if href.startswith("assignments/"):
        href = f"../{href}"
    if href.startswith("docs/"):
        href = href.removeprefix("docs/")
    return current_dir_prefix + href


def inline_markdown(text: str) -> str:
    placeholders: list[str] = []

    def keep_code(match: re.Match[str]) -> str:
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00{len(placeholders) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text)

    def link(match: re.Match[str]) -> str:
        label = match.group(1)
        href = html.unescape(match.group(2).strip())
        safe_href = html.escape(rewrite_href(href), quote=True)
        return f'<a href="{safe_href}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)

    for index, value in enumerate(placeholders):
        text = text.replace(f"\x00{index}\x00", value)
    return text


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return lines[index].strip().startswith("|") and re.match(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$", lines[index + 1])


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def render_table(lines: list[str], index: int) -> tuple[str, int]:
    headers = split_table_row(lines[index])
    index += 2
    rows: list[list[str]] = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        rows.append(split_table_row(lines[index]))
        index += 1

    head = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in headers)
    body_rows = []
    for row in rows:
        cells = row + [""] * (len(headers) - len(row))
        body_rows.append("<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in cells[: len(headers)]) + "</tr>")
    table = '<div class="table-wrap"><table><thead><tr>' + head + "</tr></thead><tbody>" + "".join(body_rows) + "</tbody></table></div>"
    return table, index


def render_markdown(markdown: str) -> tuple[str, list[tuple[int, str, str]], str]:
    lines = markdown.splitlines()
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used_slugs: set[str] = set()
    title = "课程材料"
    index = 0
    open_list: str | None = None
    open_code = False
    code_lang = ""
    code_lines: list[str] = []

    def close_list() -> None:
        nonlocal open_list
        if open_list:
            out.append(f"</{open_list}>")
            open_list = None

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if open_code:
            if stripped.startswith("```"):
                escaped = html.escape("\n".join(code_lines))
                out.append(f'<pre class="code-block" data-lang="{html.escape(code_lang)}"><code>{escaped}</code></pre>')
                open_code = False
                code_lines = []
                code_lang = ""
            else:
                code_lines.append(line)
            index += 1
            continue

        if stripped.startswith("```"):
            close_list()
            open_code = True
            code_lang = stripped.removeprefix("```").strip() or "text"
            index += 1
            continue

        if not stripped:
            close_list()
            index += 1
            continue

        if is_table_start(lines, index):
            close_list()
            table_html, index = render_table(lines, index)
            out.append(table_html)
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            close_list()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 1:
                title = text
            slug = slugify(re.sub(r"`([^`]+)`", r"\1", text), used_slugs)
            toc.append((level, slug, text))
            html_level = min(level + 1, 5)
            out.append(f'<h{html_level} id="{slug}">{inline_markdown(text)}</h{html_level}>')
            index += 1
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        if bullet or ordered:
            list_type = "ul" if bullet else "ol"
            if open_list != list_type:
                close_list()
                out.append(f"<{list_type}>")
                open_list = list_type
            item_text = (bullet or ordered).group(1)
            out.append(f"<li>{inline_markdown(item_text)}</li>")
            index += 1
            continue

        close_list()
        out.append(f"<p>{inline_markdown(stripped)}</p>")
        index += 1

    close_list()
    if open_code:
        escaped = html.escape("\n".join(code_lines))
        out.append(f'<pre class="code-block" data-lang="{html.escape(code_lang)}"><code>{escaped}</code></pre>')
    return "\n".join(out), toc, title


def render_page(markdown: str, source_name: str) -> str:
    body, toc, title = render_markdown(markdown)
    page_name = source_name.replace(".md", ".html")
    toc_items = "\n".join(
        f'<li class="doc-toc-level-{level}"><a href="#{slug}">{html.escape(text)}</a></li>'
        for level, slug, text in toc
        if level <= 3
    )
    toc_html = f'<nav class="toc"><h4>目录</h4><ol>{toc_items}</ol></nav>' if toc_items else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<link rel="icon" type="image/svg+xml" href="../images/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="../images/favicon.png">
<link rel="apple-touch-icon" href="../images/favicon.png">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{html.escape(title)} — LLM 深度学习</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body data-doc="{html.escape(page_name)}">
<aside class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <h1>LLM 深度学习</h1>
    <p>课程材料</p>
  </div>
  <nav class="sidebar-nav">
    <a href="../index.html"><span class="ch-num">⌂</span>课程首页</a>
    <a href="reading-list.html"><span class="ch-num">R</span>Reading List</a>
    <a href="written-problem-set.html"><span class="ch-num">W</span>书面题库</a>
    <a href="worked-example-pack.html"><span class="ch-num">E</span>Worked Examples</a>
  </nav>
  <div class="sidebar-footer">
    <button class="theme-toggle" onclick="LLM.toggleTheme()" aria-label="切换主题">
      <span id="theme-icon">🌙</span> <span id="theme-label">暗色模式</span>
    </button>
  </div>
</aside>
<main class="main doc-main">
  <article class="chapter doc-article">
    <div class="reading-time"><a href="../index.html">课程首页</a> / {html.escape(page_name)}</div>
    <h2>{html.escape(title)}</h2>
    {toc_html}
    <section class="card doc-content">
{body}
    </section>
  </article>
</main>
<button class="back-to-top" id="back-to-top" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
<script src="../js/db.js"></script>
<script src="../js/app.js"></script>
</body>
</html>
"""


def render_docs(source_dir: Path, out_dir: Path) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[str] = []
    for doc in DOCS:
        source = source_dir / doc
        if not source.exists():
            continue
        html_text = render_page(source.read_text(encoding="utf-8"), doc)
        target = out_dir / doc.replace(".md", ".html")
        target.write_text(html_text, encoding="utf-8")
        rendered.append(str(target))
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render docs/*.md to styled docs/*.html")
    parser.add_argument("--source", type=Path, default=ROOT / "docs")
    parser.add_argument("--out", type=Path, default=ROOT / "docs")
    args = parser.parse_args()
    for path in render_docs(args.source, args.out):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
