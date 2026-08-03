from __future__ import annotations

import argparse
import json

from .formula import OBJECTIVES, rank_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline materials formula triage")
    parser.add_argument("--formula", nargs="+", required=True)
    parser.add_argument("--objective", choices=OBJECTIVES, default="battery")
    args = parser.parse_args()
    print(json.dumps(rank_candidates(args.formula, objective=args.objective), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
