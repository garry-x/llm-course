#!/usr/bin/env python3
"""Verify that the CS224N public page still supports the local benchmark snapshot.

Default usage fetches the Stanford CS224N homepage. For CI/offline checks, pass
--html-file with a saved page or fixture. The script emits a JSON manifest so an
instructor can archive the evidence with the course operations log.
"""

from __future__ import annotations

import argparse
import datetime as dt
from html.parser import HTMLParser
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


CS224N_URL = "https://web.stanford.edu/class/cs224n/"
DEFAULT_TIMEOUT_SECONDS = 20
EXPECTED_MARKERS = [
    "CS224N: Natural Language Processing with Deep Learning",
    "Stanford / Winter 2026",
    "Assignments (48%)",
    "Assignment 1 (6%): Introduction to word vectors",
    "Assignment 2 (14%): Neural network foundations",
    "Assignment 3 (14%): Self-attention and Transformers",
    "Assignment 4 (14%): Large language model benchmarking and evaluation",
    "Final Project (49%)",
    "Project proposal (8%)",
    "Project milestone (6%)",
    "Project poster (3%)",
    "Project report (32%)",
    "Participation (3%)",
    "Late Days",
    "Regrade Requests",
    "AI Tools Policy",
    "History of NLP",
    "Word Vectors",
    "Python Review Session",
    "Backpropagation and Neural Network Basics",
    "PyTorch Tutorial Session",
    "Transformers",
    "Final Projects: Custom and Default",
    "Pretraining (Scaling, Systems, Data)",
    "Post-training (RLHF, SFT, DPO)",
    "Efficient Adaptation (Prompting + PEFT)",
    "Agents, Tool Use, and RAG",
    "Hugging Face Transformers Tutorial Session",
    "Benchmarking and Evaluation",
    "Reasoning 1",
    "Reasoning 2",
    "Tokenization and Multilinguality",
    "Interpretability",
    "Social and Broader Impacts of NLP",
    "Multimodality",
    "Tinker and LoRA Without Regret",
    "Open Questions in NLP 2026",
    "Final Project Poster Session",
]


class VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_stack: list[str] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self.skip_stack.append(tag.lower())

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self.skip_stack) - 1, -1, -1):
            if self.skip_stack[index] == tag:
                del self.skip_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if not self.skip_stack:
            self.parts.append(data)


def normalize_text(text: str) -> str:
    text = text.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_visible_text(html: str) -> str:
    parser = VisibleTextParser()
    parser.feed(html)
    return normalize_text(" ".join(parser.parts))


def fetch_html(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": "llm-course-cs224n-snapshot-verifier/1.0"})
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    if args.html_file:
        source = str(Path(args.html_file))
        html = Path(args.html_file).read_text(encoding="utf-8")
        source_mode = "html_file"
    else:
        source = args.url
        html = fetch_html(args.url, args.timeout)
        source_mode = "url"

    visible_text = extract_visible_text(html)
    matched = [marker for marker in EXPECTED_MARKERS if marker in visible_text]
    missing = [marker for marker in EXPECTED_MARKERS if marker not in visible_text]
    status = "pass" if not missing else "fail"
    fetched_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    return {
        "mode": "cs224n_current_snapshot_verification",
        "status": status,
        "source": source,
        "source_mode": source_mode,
        "source_type": "course_page",
        "accessed_at_utc": fetched_at,
        "expected_marker_count": len(EXPECTED_MARKERS),
        "matched_marker_count": len(matched),
        "missing_marker_count": len(missing),
        "matched_markers": matched,
        "missing_markers": missing,
        "next_actions": [
            "If status is fail, inspect the official page and update cs224n-current-benchmark-snapshot.md.",
            "Archive this JSON manifest in the course operations log before each live offering.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=CS224N_URL, help="CS224N public page URL")
    parser.add_argument("--html-file", help="use a local HTML file instead of fetching --url")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="network timeout in seconds")
    parser.add_argument("--json-out", help="optional manifest output path")
    args = parser.parse_args()

    manifest = build_manifest(args)
    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if manifest["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
