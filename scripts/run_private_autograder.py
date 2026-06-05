#!/usr/bin/env python3
"""Run instructor-side assignment autograder checks and emit an audit manifest.

The repository does not store real hidden tests. In a live course, pass
--hidden-dir pointing at an instructor-only directory with per-assignment
tests.py files. This script keeps public and hidden runs in one auditable
manifest without adding hidden inputs to the student release tree.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENTS = ROOT / "assignments"
DEFAULT_HIDDEN_DIR = ROOT / "private_autograder" / "hidden_tests"
ASSIGNMENT_NAMES = [
    "ch01_bpe",
    "ch02_embeddings",
    "ch03_attention",
    "ch04_multihead",
    "ch05_block",
    "ch06_gpt",
    "ch07_training",
    "ch08_generation",
    "ch09_alignment",
    "ch10_inference",
    "ch11_classic_nlp",
]


def run_suite(test_file: Path, cwd: Path, student_module: str, timeout: int) -> dict[str, Any]:
    env = os.environ.copy()
    env.setdefault("CUDA_VISIBLE_DEVICES", "")
    env["STUDENT_MODULE"] = student_module
    env["PYTHONPATH"] = os.pathsep.join(
        str(path) for path in (cwd, ROOT, Path(env.get("PYTHONPATH", ""))) if str(path)
    )
    started = time.monotonic()
    result = subprocess.run(
        [sys.executable, str(test_file)],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout,
    )
    elapsed = round(time.monotonic() - started, 3)
    return {
        "status": "pass" if result.returncode == 0 else "fail",
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "stdout_tail": result.stdout.splitlines()[-20:],
        "stderr_tail": result.stderr.splitlines()[-20:],
    }


def assignment_result(
    name: str,
    student_module: str,
    hidden_dir: Path,
    public_only: bool,
    timeout: int,
) -> dict[str, Any]:
    assignment_dir = ASSIGNMENTS / name
    public_tests = assignment_dir / "tests.py"
    if not public_tests.exists():
        raise FileNotFoundError(f"missing public tests for {name}: {public_tests}")

    result: dict[str, Any] = {
        "assignment_id": name,
        "student_module": student_module,
        "public_tests": run_suite(public_tests.name, assignment_dir, student_module, timeout),
        "hidden_tests": {
            "status": "skipped_public_only" if public_only else "not_configured",
            "source": str(hidden_dir / name / "tests.py"),
        },
        "manual_review_required": [
            "written_answers",
            "run_log",
            "honor_statement",
            "code_quality_and_hardcoding",
        ],
        "rubric_channels": [
            "public_unit_tests",
            "hidden_boundary_tests",
            "hidden_property_tests",
            "written_explanation_code_quality",
        ],
    }

    hidden_tests = hidden_dir / name / "tests.py"
    if not public_only and hidden_tests.exists():
        result["hidden_tests"] = run_suite(hidden_tests, assignment_dir, student_module, timeout)
        result["hidden_tests"]["source"] = str(hidden_tests)

    result["status"] = (
        "pass"
        if result["public_tests"]["status"] == "pass"
        and result["hidden_tests"]["status"] in {"pass", "skipped_public_only", "not_configured"}
        else "fail"
    )
    return result


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    names = [args.chapter] if args.chapter else ASSIGNMENT_NAMES
    hidden_dir = Path(args.hidden_dir).resolve()
    assignments = [
        assignment_result(
            name=name,
            student_module=args.student_module,
            hidden_dir=hidden_dir,
            public_only=args.public_only,
            timeout=args.timeout,
        )
        for name in names
    ]
    return {
        "mode": "private_autograder_public_dry_run" if args.public_only else "private_autograder",
        "student_module": args.student_module,
        "hidden_dir": str(hidden_dir),
        "hidden_tests_stored_in_repo": False,
        "student_release_excludes": ["reference_solution.py", "private_autograder/", "hidden_tests/"],
        "assignments": assignments,
        "summary": {
            "assignment_count": len(assignments),
            "pass_count": sum(1 for item in assignments if item["status"] == "pass"),
            "fail_count": sum(1 for item in assignments if item["status"] == "fail"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", choices=ASSIGNMENT_NAMES, help="run one assignment")
    parser.add_argument("--student-module", default="reference_solution", help="module imported by tests")
    parser.add_argument("--hidden-dir", default=str(DEFAULT_HIDDEN_DIR), help="instructor-only hidden tests root")
    parser.add_argument("--public-only", action="store_true", help="skip hidden tests and run public tests only")
    parser.add_argument("--timeout", type=int, default=120, help="timeout per suite in seconds")
    parser.add_argument("--json-out", help="optional manifest output path")
    args = parser.parse_args()

    manifest = build_manifest(args)
    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if manifest["summary"]["fail_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
