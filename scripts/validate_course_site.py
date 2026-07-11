#!/usr/bin/env python3
"""Validate local routes and learner-release boundaries for the static course site.

The course has parallel English and Chinese routes, generated handouts, and a
learner release that intentionally omits reference solutions. This lightweight
check uses only the standard library so it can run in local maintenance and in
the release builder without adding a web stack dependency.
"""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


CHAPTERS = [f"ch{index:02d}.html" for index in range(1, 12)]
SKIP_SCHEMES = {"data", "javascript", "mailto", "tel"}
LINK_ATTRIBUTES = {"href", "src", "data-home-href", "data-language-href"}
IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".polish-cache",
    ".translation-cache",
    ".venv",
    "__pycache__",
    "dist",
    "node_modules",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name == "id" and value:
                self.ids.add(value)
            if name in LINK_ATTRIBUTES and value:
                self.links.append((name, value))


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def is_external(href: str) -> bool:
    parsed = urlsplit(href)
    return bool(parsed.scheme) or href.startswith("//")


def resolve_target(root: Path, page: Path, raw_path: str) -> Path:
    candidate = (page.parent / unquote(raw_path)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"escapes site root: {raw_path}") from error
    return candidate


def page_ids(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        cache[path] = parse_page(path).ids
    return cache[path]


def is_course_file(root: Path, path: Path) -> bool:
    return not any(part in IGNORED_DIRECTORY_NAMES for part in path.relative_to(root).parts)


def validate_site(root: Path, learner_release: bool = False) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        return [f"site root does not exist: {root}"]

    required_pages = [root / "index.html", root / "en.html", root / "zh" / "index.html"]
    for directory in (root / "chapters", root / "zh" / "chapters"):
        required_pages.extend(directory / chapter for chapter in CHAPTERS)
    for path in required_pages:
        if not path.is_file():
            errors.append(f"missing required route: {path.relative_to(root)}")

    id_cache: dict[Path, set[str]] = {}
    html_pages = sorted(path for path in root.rglob("*.html") if is_course_file(root, path))
    for page in html_pages:
        relative_page = page.relative_to(root)
        try:
            parsed_page = parse_page(page)
        except UnicodeDecodeError as error:
            errors.append(f"cannot decode {relative_page}: {error}")
            continue

        for attribute, href in parsed_page.links:
            if href.startswith("#"):
                target = page
                fragment = href[1:]
            elif is_external(href):
                scheme = urlsplit(href).scheme.lower()
                if scheme in SKIP_SCHEMES or scheme in {"http", "https"}:
                    continue
                continue
            else:
                parts = urlsplit(href)
                if parts.scheme.lower() in SKIP_SCHEMES:
                    continue
                raw_path = parts.path
                fragment = parts.fragment
                if not raw_path:
                    target = page
                else:
                    try:
                        target = resolve_target(root, page, raw_path)
                    except ValueError as error:
                        errors.append(f"{relative_page}: {attribute}={href!r} {error}")
                        continue

            if not target.exists():
                errors.append(f"{relative_page}: missing local target for {attribute}={href!r}")
                continue

            if fragment and target.is_file() and target.suffix.lower() == ".html":
                if fragment not in page_ids(target, id_cache):
                    errors.append(
                        f"{relative_page}: missing anchor #{fragment} in {target.relative_to(root)}"
                    )

    if learner_release:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or not is_course_file(root, path):
                continue
            if path.name == "reference_solution.py":
                errors.append(f"{path.relative_to(root)}: learner release contains a reference solution file")
            if path.suffix.lower() == ".html":
                text = path.read_text(encoding="utf-8")
                for marker in ('class="solution"', 'class="solution-toggle"'):
                    if marker in text:
                        errors.append(
                            f"{path.relative_to(root)}: learner release contains forbidden marker {marker!r}"
                        )
                        break

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--learner-release",
        action="store_true",
        help="also reject inline reference solutions and reference_solution.py",
    )
    args = parser.parse_args()
    errors = validate_site(args.root, learner_release=args.learner_release)
    if errors:
        print(f"COURSE SITE VALIDATION: FAIL ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"COURSE SITE VALIDATION: PASS ({args.root.resolve()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
