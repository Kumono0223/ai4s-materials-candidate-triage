from __future__ import annotations

import argparse
import json

from .formula import analyze_formula


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline materials formula triage")
    parser.add_argument("--formula", nargs="+", required=True)
    args = parser.parse_args()
    results = sorted((analyze_formula(formula) for formula in args.formula), key=lambda item: item["triage_score"], reverse=True)
    print(json.dumps({"candidates": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

