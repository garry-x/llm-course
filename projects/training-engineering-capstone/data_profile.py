import argparse
import json
from collections import Counter
from pathlib import Path


def percentile(values: list[int], pct: float) -> int:
    if not values:
        return 0
    values = sorted(values)
    idx = min(len(values) - 1, int((pct / 100) * (len(values) - 1)))
    return values[idx]


def audit(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    lengths = [len(line) for line in lines]
    non_empty = [line for line in lines if line.strip()]
    counts = Counter(non_empty)
    duplicate_lines = sum(count - 1 for count in counts.values() if count > 1)
    text = "\n".join(lines)
    chars = sorted(set(text))
    return {
        "file": str(path),
        "lines": len(lines),
        "empty_lines": sum(1 for line in lines if not line.strip()),
        "duplicate_non_empty_lines": duplicate_lines,
        "characters": len(text),
        "unique_chars": len(chars),
        "length_p50": percentile(lengths, 50),
        "length_p95": percentile(lengths, 95),
        "length_max": max(lengths) if lengths else 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a text dataset before LLM training")
    parser.add_argument("--data", default="sample_corpus.txt")
    args = parser.parse_args()
    print(json.dumps(audit(Path(args.data)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
