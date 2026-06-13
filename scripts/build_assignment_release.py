#!/usr/bin/env python3
"""Build student-facing assignment release bundles.

The source tree keeps reference_solution.py for instructor validation and
self-study. Formal course releases should exclude it.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENTS = [
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
INCLUDED_FILES = ["README.md", "starter.py", "tests.py"]
EXCLUDED_FILES = ["reference_solution.py", "__pycache__"]
TEST_DEFAULT_FROM = 'os.environ.get("STUDENT_MODULE", "reference_solution")'
TEST_DEFAULT_TO = 'os.environ.get("STUDENT_MODULE", "student_solution")'
RELEASE_NOTICE = """\
## Student Release Notes

This student-facing release excludes instructor reference solutions and hidden tests.

```bash
cp starter.py student_solution.py
# Edit student_solution.py, then run:
STUDENT_MODULE=student_solution ../../.venv/bin/python tests.py
```

"""


def assignment_manifest(name: str) -> dict[str, object]:
    src = ROOT / "assignments" / name
    if not src.exists():
        raise FileNotFoundError(f"missing assignment directory: {src}")
    missing = [file_name for file_name in INCLUDED_FILES if not (src / file_name).exists()]
    if missing:
        raise FileNotFoundError(f"{name} missing release files: {missing}")
    return {
        "assignment": name,
        "included": INCLUDED_FILES,
        "excluded": EXCLUDED_FILES,
        "test_default_module": "student_solution",
    }


def rewrite_tests_for_student_release(text: str) -> str:
    if TEST_DEFAULT_FROM not in text:
        raise ValueError("tests.py does not contain expected STUDENT_MODULE default")
    text = text.replace(TEST_DEFAULT_FROM, TEST_DEFAULT_TO)
    text = text.replace("reference_solution.py", "student_solution.py")
    text = text.replace("reference_solution", "student_solution")
    return text


def rewrite_readme_for_student_release(text: str) -> str:
    cleaned_lines: list[str] = []
    skip_fence = False
    for line in text.splitlines():
        if skip_fence:
            if line.strip() == "```":
                skip_fence = False
            continue
        if "reference_solution" in line or "reference implementation" in line or "built-in course reference" in line:
            if "```" not in line:
                skip_fence = "default tests" in line or "built-in course reference" in line
            continue
        cleaned_lines.append(line)
    cleaned = "\n".join(cleaned_lines).strip() + "\n\n"
    return cleaned + RELEASE_NOTICE


def build_assignment(name: str, out_dir: Path) -> dict[str, object]:
    manifest = assignment_manifest(name)
    src = ROOT / "assignments" / name
    dst = out_dir / name
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    for file_name in INCLUDED_FILES:
        source = src / file_name
        target = dst / file_name
        if file_name == "tests.py":
            target.write_text(
                rewrite_tests_for_student_release(source.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        elif file_name == "README.md":
            target.write_text(
                rewrite_readme_for_student_release(source.read_text(encoding="utf-8")),
                encoding="utf-8",
            )
        else:            shutil.copy2(source, target)

    (dst / "RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assignment", nargs="?", choices=ASSIGNMENTS, help="assignment to package")
    parser.add_argument("--all", action="store_true", help="package all assignments")
    parser.add_argument("--out", default="dist/assignments", help="output directory")
    parser.add_argument("--dry-run", action="store_true", help="print manifest without writing files")
    args = parser.parse_args()

    if args.all == bool(args.assignment):
        parser.error("choose exactly one of ASSIGNMENT or --all")

    names = ASSIGNMENTS if args.all else [args.assignment]
    manifests = [assignment_manifest(name) for name in names]
    result = {"out": args.out, "assignments": manifests}

    if not args.dry_run:
        out_dir = ROOT / args.out
        out_dir.mkdir(parents=True, exist_ok=True)
        result["assignments"] = [build_assignment(name, out_dir) for name in names]

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
