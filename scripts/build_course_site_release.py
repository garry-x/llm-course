#!/usr/bin/env python3
"""Build a student-facing static course site without inline reference solutions."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [f"ch{index:02d}.html" for index in range(1, 11)]
SAFE_DOCS = [
    "accessibility-student-support.md",
    "academic-integrity-case-process.md",
    "assessment-administration-policy.md",
    "assessment-blueprint-coverage-matrix.md",
    "assessment-item-analysis-psychometrics.md",
    "assessment-item-bank-ledger.md",
    "assignment-handout-pack.md",
    "assignment-submission-guide.md",
    "capstone-defense-oral-exam-bank.md",
    "capstone-project-gallery.md",
    "capstone-proposal-milestone.md",
    "chapter-claim-audit-ledger.md",
    "chapter-source-map.md",
    "claim-audit-worksheet.md",
    "classic-nlp-deep-dive-module.md",
    "classic-nlp-handout.md",
    "concept-misconception-map.md",
    "comprehensive-review-study-guide.md",
    "course-communication-policy.md",
    "course-errata-correction-ledger.md",
    "course-calendar-deadline-ledger.md",
    "compute-resource-guide.md",
    "core-concept-glossary.md",
    "course-materials-index.md",
    "course-outcome-map.md",
    "course-policies.md",
    "course-staff-office-hours-directory.md",
    "cs224n-benchmark-crosswalk.md",
    "cs224n-current-benchmark-snapshot.md",
    "data-ethics-review.md",
    "dataset-model-artifact-registry.md",
    "default-final-project-guide.md",
    "environment-reproducibility.md",
    "enrollment-audit-public-use-policy.md",
    "external-source-inventory.md",
    "external-source-verification.md",
    "external-expert-review-dossier.md",
    "experimental-rigor-evaluation-statistics.md",
    "final-project-showcase-archive-policy.md",
    "frontier-seminar-handout.md",
    "frontier-source-evidence-cards.md",
    "frontier-source-audit.md",
    "gradebook-lms-operations.md",
    "guest-speaker-seminar-policy.md",
    "inference-engineer-curriculum.md",
    "lecture-media-access-policy.md",
    "lecture-note-sample-pack.md",
    "learning-outcome-attainment-report.md",
    "learning-analytics-remediation-plan.md",
    "lecture-notes-review-ledger.md",
    "lecture-notes-quality-review.md",
    "lecture-slide-sample-pack.md",
    "mathematical-derivation-audit.md",
    "material-versioning-archive-policy.md",
    "math-prerequisites.md",
    "midterm-final-review-pack.md",
    "ml-foundations-prerequisite-bridge.md",
    "model-benchmark-card-guide.md",
    "notation-shape-glossary.md",
    "nlp-evaluation-coverage.md",
    "participation-feedback-guide.md",
    "paper-recap-calibration-pack.md",
    "paper-to-code-traceability-matrix.md",
    "presentation-peer-review.md",
    "presemester-readiness-audit.md",
    "prerequisite-diagnostic.md",
    "programming-assignment-code-quality-rubric.md",
    "python-pytorch-review-session.md",
    "reading-discussion-question-bank.md",
    "project-team-mentor-policy.md",
    "project-submission-dossier.md",
    "project-report-rubric.md",
    "project-report-exemplar-pack.md",
    "project-report-template.md",
    "quiz-checkpoint-guide.md",
    "recitation-worksheet-pack.md",
    "reading-list.md",
    "safety-societal-impact-casebook.md",
    "staff-assistance-code-review-policy.md",
    "student-faq-troubleshooting.md",
    "syllabus.md",
    "teaching-observation-course-evaluation.md",
    "topic-dependency-map.md",
    "training-engineer-curriculum.md",
    "university-course-quality-audit.md",
    "weekly-teaching-reflection-adjustment-log.md",
    "workload-pacing-calibration.md",
    "worked-example-pack.md",
    "written-problem-set.md",
]
ROOT_PAGES = [
    "inference-engineer-curriculum.html",
    "training-engineer-curriculum.html",
]
PROJECT_DIRS = [
    "inference-engineering-capstone",
    "training-engineering-capstone",
]
INCLUDED_ROOTS = [
    "index.html",
    "inference-engineer-curriculum.html",
    "training-engineer-curriculum.html",
    "chapters/",
    "css/",
    "js/",
    "images/",
    "docs/",
    "assignments/",
    "projects/",
]
EXCLUDED_DOCS = [
    "autograder-hidden-tests.md",
    "board-derivation-pack.md",
    "course-operations-log.md",
    "demo-runbook.md",
    "discussion-office-hours-guide.md",
    "grading-calibration.md",
    "grading-drift-audit-ledger.md",
    "grading-anchor-sample-feedback-pack.md",
    "instructor-solution-guide.md",
    "lecture-notes-index.md",
    "lecture-plan.md",
    "lecture-slide-outline.md",
    "private-autograder-operations.md",
    "staff-runbook.md",
    "ta-training-certification.md",
]


def strip_inline_solutions(html: str) -> tuple[str, int]:
    """Remove reference-solution toggles and their adjacent solution blocks."""
    lines = html.splitlines(keepends=True)
    output: list[str] = []
    removed_blocks = 0
    skipping_solution = False
    div_depth = 0

    for line in lines:
        if 'class="solution-toggle"' in line:
            removed_blocks += 1
            continue

        if not skipping_solution and 'class="solution"' in line:
            skipping_solution = True
            div_depth = line.count("<div") - line.count("</div>")
            if div_depth <= 0:
                skipping_solution = False
            continue

        if skipping_solution:
            div_depth += line.count("<div") - line.count("</div>")
            if div_depth <= 0:
                skipping_solution = False
            continue

        output.append(line)

    return "".join(output), removed_blocks


def rewrite_internal_material_links(text: str) -> str:
    for doc in EXCLUDED_DOCS:
        escaped_doc = re.escape(doc)
        text = re.sub(
            rf'<a href="(?:\.\./)?docs/{escaped_doc}"[^>]*>(.*?)</a>',
            r"\1（教师内部材料）",
            text,
            flags=re.S,
        )
        text = re.sub(
            rf'<a href="{escaped_doc}"[^>]*>(.*?)</a>',
            r"\1（教师内部材料）",
            text,
            flags=re.S,
        )
        text = re.sub(
            rf"\[([^\]]+)\]\((?:\.\./)?docs/{escaped_doc}(?:#[^)]+)?\)",
            r"\1（教师内部材料）",
            text,
        )
        text = re.sub(
            rf"\[([^\]]+)\]\({escaped_doc}(?:#[^)]+)?\)",
            r"\1（教师内部材料）",
            text,
        )
        text = text.replace(f"`docs/{doc}`", "`教师内部材料`")
    return text


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def build_release(out_dir: Path) -> dict[str, object]:
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    index = rewrite_internal_material_links((ROOT / "index.html").read_text(encoding="utf-8"))
    (out_dir / "index.html").write_text(index, encoding="utf-8")
    for page in ROOT_PAGES:
        text = rewrite_internal_material_links((ROOT / page).read_text(encoding="utf-8"))
        (out_dir / page).write_text(text, encoding="utf-8")
    copy_tree(ROOT / "css", out_dir / "css")
    copy_tree(ROOT / "js", out_dir / "js")
    copy_tree(ROOT / "images", out_dir / "images")

    chapter_manifest = []
    for chapter in CHAPTERS:
        source = (ROOT / "chapters" / chapter).read_text(encoding="utf-8")
        stripped, removed = strip_inline_solutions(source)
        stripped = rewrite_internal_material_links(stripped)
        target = out_dir / "chapters" / chapter
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(stripped, encoding="utf-8")
        chapter_manifest.append({"file": f"chapters/{chapter}", "removed_solution_blocks": removed})

    docs_dir = out_dir / "docs"
    docs_dir.mkdir()
    for doc in SAFE_DOCS:
        text = (ROOT / "docs" / doc).read_text(encoding="utf-8")
        (docs_dir / doc).write_text(rewrite_internal_material_links(text), encoding="utf-8")

    projects_dir = out_dir / "projects"
    projects_dir.mkdir()
    for project in PROJECT_DIRS:
        copy_tree(ROOT / "projects" / project, projects_dir / project)

    assignment_release = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/build_assignment_release.py"),
            "--all",
            "--out",
            str(out_dir / "assignments"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if assignment_release.returncode != 0:
        raise RuntimeError(f"assignment release builder failed: {assignment_release.stderr.strip()}")
    try:
        assignment_manifest = json.loads(assignment_release.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"assignment release builder emitted invalid JSON: {error}") from error

    manifest = {
        "mode": "student-site",
        "description": "Static course site with inline reference solutions removed.",
        "included_roots": INCLUDED_ROOTS,
        "root_pages": ROOT_PAGES,
        "safe_docs": SAFE_DOCS,
        "excluded_docs": EXCLUDED_DOCS,
        "project_dirs": [f"projects/{project}/" for project in PROJECT_DIRS],
        "assignment_release": assignment_manifest,
        "chapters": chapter_manifest,
    }
    (out_dir / "SITE_RELEASE_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a student-facing static course site release")
    parser.add_argument("--out", required=True, type=Path, help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Print release manifest without writing files")
    args = parser.parse_args()

    manifest = {
        "mode": "student-site",
        "included_roots": INCLUDED_ROOTS,
        "root_pages": ROOT_PAGES,
        "safe_docs": SAFE_DOCS,
        "excluded_docs": EXCLUDED_DOCS,
        "project_dirs": [f"projects/{project}/" for project in PROJECT_DIRS],
        "chapters": [{"file": f"chapters/{chapter}"} for chapter in CHAPTERS],
    }
    if args.dry_run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0

    built = build_release(args.out)
    print(json.dumps(built, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
