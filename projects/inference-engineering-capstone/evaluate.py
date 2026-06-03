import argparse
import json

import httpx


def load_cases(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main(url: str, cases_path: str) -> None:
    cases = load_cases(cases_path)
    passed = 0
    details = []
    with httpx.Client(timeout=30) as client:
        for case in cases:
            resp = client.post(
                f"{url}/v1/chat/completions",
                json={
                    "model": "mock-llm",
                    "messages": [{"role": "user", "content": case["prompt"]}],
                    "max_tokens": case.get("max_tokens", 128),
                    "use_rag": case.get("use_rag", True),
                },
            )
            ok = resp.status_code == 200
            data = resp.json() if ok else {}
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            for needle in case.get("must_contain", []):
                ok = ok and needle in content
            for needle in case.get("must_retrieve", []):
                ok = ok and any(needle in doc for doc in data.get("x_retrieved_docs", []))
            passed += int(ok)
            details.append({"name": case["name"], "passed": ok})

    print(f"pass_rate: {passed}/{len(cases)} = {passed / max(len(cases), 1):.1%}")
    for item in details:
        print(f"{'PASS' if item['passed'] else 'FAIL'} {item['name']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--cases", default="eval_cases.jsonl")
    args = parser.parse_args()
    main(args.url.rstrip("/"), args.cases)
