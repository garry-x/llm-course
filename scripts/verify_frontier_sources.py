#!/usr/bin/env python3
"""Verify volatile frontier-source markers used by course evidence cards.

The script fetches official/primary pages and checks only lightweight textual
markers that support the local frontier source evidence cards. It is not a
benchmark validator and does not make model-card claims stable theory.
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


DEFAULT_TIMEOUT_SECONDS = 25
USER_AGENT = "llm-course-frontier-source-verifier/1.0"

SOURCE_CHECKS = [
    {
        "id": "deepseek_v32_exp_api_news",
        "url": "https://api-docs.deepseek.com/news/news250929",
        "source_kind": "API news",
        "supports_cards": ["FSEC-DSA-2026-0605"],
        "required_markers": [
            "Introducing DeepSeek-V3.2-Exp",
            "DeepSeek Sparse Attention",
            "long context",
            "training & inference",
            "Tech report",
            "DeepSeek-V3.2-Exp",
        ],
        "absent_markers": [],
    },
    {
        "id": "deepseek_v4_pro_model_card",
        "url": "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro",
        "source_kind": "model card",
        "supports_cards": [
            "FSEC-V4-ARCH-2026-0605",
            "FSEC-V4-EFF-2026-0605",
            "FSEC-V4-REASON-2026-0605",
            "FSEC-V4-MTP-MONITOR-2026-0605",
            "FSEC-ENGRAM-MONITOR-2026-0605",
            "FSEC-R1-UNIFY-MONITOR-2026-0605",
        ],
        "required_markers": [
            "DeepSeek-V4-Pro",
            "1.6T parameters",
            "49B activated",
            "one million tokens",
            "Compressed Sparse Attention",
            "Heavily Compressed Attention",
            "27% of single-token inference FLOPs",
            "10% of KV cache",
            "Manifold-Constrained Hyper-Connections",
            "Muon Optimizer",
            "on-policy distillation",
            "three reasoning effort modes",
        ],
        "absent_markers": [
            "Engram",
            "NIAH",
            "speculative decoding",
        ],
    },
    {
        "id": "deepseek_v2_arxiv",
        "url": "https://arxiv.org/abs/2405.04434",
        "source_kind": "technical report",
        "supports_cards": ["FSEC-V2V3-REPORTS-2026-0605"],
        "required_markers": [
            "DeepSeek-V2",
            "Mixture-of-Experts",
            "economical",
            "efficient",
        ],
        "absent_markers": [],
    },
    {
        "id": "deepseek_v3_arxiv",
        "url": "https://arxiv.org/abs/2412.19437",
        "source_kind": "technical report",
        "supports_cards": ["FSEC-V2V3-REPORTS-2026-0605"],
        "required_markers": [
            "DeepSeek-V3",
            "Technical Report",
            "Mixture-of-Experts",
            "671B",
            "37B",
        ],
        "absent_markers": [],
    },
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
    return re.sub(r"\s+", " ", text).strip()


def extract_visible_text(html: str) -> str:
    parser = VisibleTextParser()
    parser.feed(html)
    return normalize_text(" ".join(parser.parts))


def fetch_html(url: str, timeout: int) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def read_source_text(check: dict[str, Any], args: argparse.Namespace) -> tuple[str, str, str]:
    fixture_dir = Path(args.fixture_dir) if args.fixture_dir else None
    if fixture_dir:
        fixture_path = fixture_dir / f"{check['id']}.html"
        html = fixture_path.read_text(encoding="utf-8")
        return extract_visible_text(html), str(fixture_path), "fixture"
    html = fetch_html(check["url"], args.timeout)
    return extract_visible_text(html), check["url"], "url"


def evaluate_check(check: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    visible_text, source, source_mode = read_source_text(check, args)
    matched_required = [marker for marker in check["required_markers"] if marker in visible_text]
    missing_required = [marker for marker in check["required_markers"] if marker not in visible_text]
    matched_absent = [marker for marker in check["absent_markers"] if marker in visible_text]
    status = "pass" if not missing_required and not matched_absent else "fail"
    return {
        "id": check["id"],
        "status": status,
        "source": source,
        "source_mode": source_mode,
        "source_kind": check["source_kind"],
        "supports_cards": check["supports_cards"],
        "required_marker_count": len(check["required_markers"]),
        "matched_required_count": len(matched_required),
        "missing_required_count": len(missing_required),
        "absent_marker_count": len(check["absent_markers"]),
        "unexpected_absent_marker_hit_count": len(matched_absent),
        "matched_required_markers": matched_required,
        "missing_required_markers": missing_required,
        "unexpected_absent_marker_hits": matched_absent,
    }


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    checked_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    checks = [evaluate_check(check, args) for check in SOURCE_CHECKS]
    status = "pass" if all(check["status"] == "pass" for check in checks) else "fail"
    supported_cards = sorted({card for check in checks for card in check["supports_cards"]})
    return {
        "mode": "frontier_source_evidence_verification",
        "status": status,
        "checked_at_utc": checked_at,
        "check_count": len(checks),
        "passed_check_count": sum(1 for check in checks if check["status"] == "pass"),
        "supported_cards": supported_cards,
        "checks": checks,
        "next_actions": [
            "If a required marker is missing, inspect the official source and update frontier-source-evidence-cards.md.",
            "If an absent marker appears, decide whether the monitor-only claim should be upgraded with a dated evidence card.",
            "Archive this JSON manifest with the course operations log before each live offering.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="network timeout in seconds")
    parser.add_argument("--fixture-dir", help="directory containing {check_id}.html fixtures")
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
