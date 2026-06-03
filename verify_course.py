import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_CHAPTERS = 10
EXPECTED_SECTIONS = 127
EXPECTED_EXERCISES = "103"


def ok(message: str) -> None:
    print(f"PASS {message}")


def fail(message: str) -> None:
    raise RuntimeError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def check_chapter_counts() -> None:
    chapter_files = sorted((ROOT / "chapters").glob("ch*.html"))
    if len(chapter_files) != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} chapter files, got {len(chapter_files)}")

    js = read("js/app.js")
    entries = re.findall(r"\{id:(\d+), file:'(ch\d+\.html)'.*?sections:(\d+)\}", js)
    if len(entries) != EXPECTED_CHAPTERS:
        fail(f"expected {EXPECTED_CHAPTERS} CHAPTERS entries in js/app.js, got {len(entries)}")

    total = 0
    for _, file_name, declared in entries:
        html = read(f"chapters/{file_name}")
        ids = re.findall(r'<section class="card" id="([^"]+)"', html)
        unique_ids = set(ids)
        if len(ids) != len(unique_ids):
            fail(f"{file_name} has duplicate section ids")
        if len(ids) != int(declared):
            fail(f"{file_name} declares {declared} sections in js/app.js but has {len(ids)}")
        total += len(ids)

    if total != EXPECTED_SECTIONS:
        fail(f"expected {EXPECTED_SECTIONS} total sections, got {total}")
    ok(f"chapter metadata matches {EXPECTED_CHAPTERS} chapters / {EXPECTED_SECTIONS} sections")


def check_public_stats() -> None:
    readme = read("README.md")
    index = read("index.html")
    required = [
        (readme, f"sections-{EXPECTED_SECTIONS}-yellow", "README section badge"),
        (readme, f"{EXPECTED_SECTIONS} 小节", "README section total"),
        (readme, f"exercises-{EXPECTED_EXERCISES}", "README exercise badge"),
        (index, f"{EXPECTED_SECTIONS} 小节", "index section total"),
        (index, f"{EXPECTED_EXERCISES} 道", "index exercise total"),
        (index, "inference-engineer-curriculum.html", "index graduation roadmap link"),
        (index, "training-engineer-curriculum.html", "index training roadmap link"),
        (readme, "projects/inference-engineering-capstone/", "README capstone link"),
        (readme, "projects/training-engineering-capstone/", "README training capstone link"),
    ]
    for content, needle, label in required:
        if needle not in content:
            fail(f"missing {label}: {needle}")
    ok("public stats and course links are present")


def check_capstone_files() -> None:
    capstone = ROOT / "projects/inference-engineering-capstone"
    required = [
        "acceptance.py",
        "app.py",
        "benchmark.py",
        "capacity_plan.py",
        "evaluate.py",
        "slo_check.py",
        "eval_cases.jsonl",
        "requirements.txt",
        "README.md",
    ]
    for name in required:
        if not (capstone / name).exists():
            fail(f"missing capstone file: {name}")

    for path in sorted(capstone.glob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")

    cases = 0
    for line in (capstone / "eval_cases.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            json.loads(line)
            cases += 1
    if cases < 5:
        fail(f"expected at least 5 capstone eval cases, got {cases}")
    ok(f"capstone files compile and {cases} eval cases are valid")


def check_training_capstone_files() -> None:
    capstone = ROOT / "projects/training-engineering-capstone"
    required = [
        "acceptance.py",
        "data_audit.py",
        "plan_training.py",
        "train.py",
        "sample_corpus.txt",
        "requirements.txt",
        "README.md",
    ]
    for name in required:
        if not (capstone / name).exists():
            fail(f"missing training capstone file: {name}")

    for path in sorted(capstone.glob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")

    corpus = (capstone / "sample_corpus.txt").read_text(encoding="utf-8")
    if len(corpus) < 128:
        fail("training capstone sample corpus is too small")
    ok("training capstone files compile and sample corpus is present")


def check_javascript() -> None:
    result = subprocess.run(["node", "--check", "js/app.js"], cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        fail("node --check js/app.js failed")
    ok("js/app.js syntax is valid")


def run_capstone_acceptance() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "acceptance.py",
            "--port",
            "8023",
            "--requests",
            "4",
            "--concurrency",
            "2",
            "--min-tokens-per-second",
            "100",
        ],
        cwd=ROOT / "projects/inference-engineering-capstone",
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        fail("capstone acceptance failed")
    ok("capstone acceptance passed")


def run_training_acceptance() -> None:
    result = subprocess.run(
        [sys.executable, "acceptance.py"],
        cwd=ROOT / "projects/training-engineering-capstone",
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode != 0:
        fail("training capstone acceptance failed")
    ok("training capstone acceptance passed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify course metadata, scripts, and optional capstone acceptance")
    parser.add_argument("--capstone", action="store_true", help="Run the full inference Capstone acceptance flow")
    parser.add_argument("--training", action="store_true", help="Run the PyTorch training Capstone acceptance flow")
    args = parser.parse_args()

    check_chapter_counts()
    check_public_stats()
    check_capstone_files()
    check_training_capstone_files()
    check_javascript()
    if args.capstone:
        run_capstone_acceptance()
    if args.training:
        run_training_acceptance()
    print("COURSE VERIFY: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"COURSE VERIFY: FAIL ({exc})", file=sys.stderr)
        sys.exit(1)
