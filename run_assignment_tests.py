"""Run chapter assignment test suites.

Default behavior runs each assignment test suite against its bundled
reference_solution.py. This proves the autograder-style tests are executable.
Students can run a single suite against their own module by invoking that
suite directly with STUDENT_MODULE=...
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ASSIGNMENTS = ROOT / "assignments"


def discover_suites(chapter=None):
    suites = []
    for path in sorted(ASSIGNMENTS.glob("ch*/tests.py")):
        if chapter and path.parent.name != chapter:
            continue
        suites.append(path)
    return suites


def main():
    parser = argparse.ArgumentParser(description="Run bundled chapter assignment tests")
    parser.add_argument("--chapter", help="Run one suite, e.g. ch01_bpe")
    args = parser.parse_args()

    suites = discover_suites(args.chapter)
    if not suites:
        raise SystemExit(f"No assignment tests found for chapter={args.chapter!r}")

    failed = 0
    for suite in suites:
        rel = suite.relative_to(ROOT)
        print(f"== {rel} ==")
        env = os.environ.copy()
        env.setdefault("CUDA_VISIBLE_DEVICES", "")
        result = subprocess.run(
            [sys.executable, suite.name],
            cwd=suite.parent,
            env=env,
            text=True,
        )
        if result.returncode != 0:
            failed += 1

    if failed:
        raise SystemExit(f"{failed} assignment test suite(s) failed")
    print(f"ASSIGNMENT TESTS: PASS ({len(suites)} suite(s))")


if __name__ == "__main__":
    main()
