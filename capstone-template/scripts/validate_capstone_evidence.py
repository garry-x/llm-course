#!/usr/bin/env python3
"""Check the evidence package for a copied LLM course capstone template.

This checker enforces completeness and traceability, not universal product
thresholds. Learners define their quality, safety, latency, and cost gates in
the project contract, then record evidence for the resulting decision.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\[REPLACE\s*:", re.IGNORECASE)
REQUIRED_CONTRACT_HEADINGS = {
    "user task",
    "output and permission boundary",
    "baseline",
    "primary intervention",
    "success metrics and evaluation boundary",
    "reject / rollback rule",
}
REQUIRED_REPORT_HEADINGS = {
    "question and scope",
    "baseline and intervention",
    "evaluation and results",
    "failures and limits",
    "release decision",
}
REQUIRED_MANIFEST_FIELDS = {
    "record_id",
    "split",
    "data_version",
    "source_version",
    "content_type",
    "permission_status",
    "owner",
    "contains_sensitive_data",
    "deletion_or_update_path",
}
REQUIRED_EVAL_FIELDS = {
    "case_id",
    "slice",
    "input",
    "expected_behavior",
    "risk_level",
    "source_version",
    "frozen",
}
REQUIRED_DRILL_FIELDS = {
    "drill_id",
    "category",
    "input_or_event",
    "expected_control",
    "observed_outcome",
    "status",
    "evidence_ref",
}
REQUIRED_RUN_FIELDS = {
    "run_id",
    "role",
    "commit",
    "command",
    "seed",
    "hardware_or_runtime",
    "model_or_pipeline_version",
    "tokenizer_or_template_version",
    "data_or_index_version",
    "evaluation_version",
    "metrics",
    "resource_profile",
}
REQUIRED_METRICS = {"quality", "safety", "latency", "cost"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def contains_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return bool(PLACEHOLDER_RE.search(value))
    if isinstance(value, dict):
        return any(contains_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_placeholder(item) for item in value)
    return False


def headings(text: str) -> set[str]:
    return {
        match.group(1).strip().lower()
        for match in re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
    }


def read_text(path: Path, errors: list[str]) -> str | None:
    if not path.is_file():
        errors.append(f"missing required file: {path}")
        return None
    text = path.read_text(encoding="utf-8")
    if contains_placeholder(text):
        errors.append(f"unreplaced template placeholder in {path}")
    return text


def read_jsonl(path: Path, required_fields: set[str], label: str, errors: list[str]) -> list[dict[str, Any]]:
    text = read_text(path, errors)
    if text is None:
        return []
    records: list[dict[str, Any]] = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            errors.append(f"{path}:{number}: invalid JSONL record: {error.msg}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{path}:{number}: {label} record must be an object")
            continue
        missing = sorted(required_fields - record.keys())
        if missing:
            errors.append(f"{path}:{number}: {label} record missing {', '.join(missing)}")
        if contains_placeholder(record):
            errors.append(f"{path}:{number}: {label} record has an unreplaced template placeholder")
        records.append(record)
    if not records:
        errors.append(f"{path}: expected at least one {label} record")
    return records


def validate_markdown(path: Path, required: set[str], label: str, errors: list[str]) -> None:
    text = read_text(path, errors)
    if text is None:
        return
    missing = sorted(required - headings(text))
    if missing:
        errors.append(f"{path}: {label} missing headings: {', '.join(missing)}")


def validate_run(path: Path, errors: list[str]) -> dict[str, Any] | None:
    text = read_text(path, errors)
    if text is None:
        return None
    try:
        record = json.loads(text)
    except json.JSONDecodeError as error:
        errors.append(f"{path}: invalid JSON: {error.msg}")
        return None
    if not isinstance(record, dict):
        errors.append(f"{path}: run record must be an object")
        return None
    missing = sorted(REQUIRED_RUN_FIELDS - record.keys())
    if missing:
        errors.append(f"{path}: run record missing {', '.join(missing)}")
    metrics = record.get("metrics")
    if not isinstance(metrics, dict):
        errors.append(f"{path}: metrics must be an object")
    else:
        missing_metrics = sorted(REQUIRED_METRICS - metrics.keys())
        if missing_metrics:
            errors.append(f"{path}: metrics missing {', '.join(missing_metrics)}")
    if contains_placeholder(record):
        errors.append(f"{path}: run record has an unreplaced template placeholder")
    return record


def validate_project(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    if not root.is_dir():
        return [f"project directory does not exist: {root}"]

    validate_markdown(root / "project_contract.md", REQUIRED_CONTRACT_HEADINGS, "project contract", errors)
    manifest = read_jsonl(root / "data_manifest.jsonl", REQUIRED_MANIFEST_FIELDS, "manifest", errors)
    eval_cases = read_jsonl(root / "eval" / "cases.jsonl", REQUIRED_EVAL_FIELDS, "evaluation", errors)
    drills = read_jsonl(root / "safety" / "drills.jsonl", REQUIRED_DRILL_FIELDS, "safety drill", errors)
    validate_markdown(root / "reports" / "decision.md", REQUIRED_REPORT_HEADINGS, "decision report", errors)

    for record in manifest:
        if record.get("split") not in {"train", "dev", "test", "retrieval_corpus", "preference", "synthetic"}:
            errors.append(f"data manifest record {record.get('record_id', '<unknown>')!r}: unsupported split")
        if not isinstance(record.get("contains_sensitive_data"), bool):
            errors.append(f"data manifest record {record.get('record_id', '<unknown>')!r}: contains_sensitive_data must be boolean")
    for record in eval_cases:
        if record.get("frozen") is not True:
            errors.append(f"evaluation case {record.get('case_id', '<unknown>')!r}: frozen must be true")
    for record in drills:
        if record.get("status") != "pass":
            errors.append(f"safety drill {record.get('drill_id', '<unknown>')!r}: status must be pass before release")

    runs_dir = root / "runs"
    runs = [validate_run(path, errors) for path in sorted(runs_dir.glob("*.json"))] if runs_dir.is_dir() else []
    runs = [run for run in runs if run is not None]
    if not runs:
        errors.append(f"{runs_dir}: expected at least one baseline and one variant run record")
    roles = {run.get("role") for run in runs}
    missing_roles = {"baseline", "variant"} - roles
    if missing_roles:
        errors.append(f"{runs_dir}: missing run role(s): {', '.join(sorted(missing_roles))}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="copied capstone project directory")
    args = parser.parse_args()
    errors = validate_project(args.project)
    if errors:
        print(f"CAPSTONE EVIDENCE: FAIL ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"CAPSTONE EVIDENCE: PASS ({args.project.resolve()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
