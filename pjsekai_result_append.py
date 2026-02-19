Python 3.14.3 (tags/v3.14.3:323c59a, Feb  3 2026, 16:04:56) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
#!/usr/bin/env python3
"""Append Project Sekai result entries to a CSV file.

Usage examples:
  python pjsekai_result_append.py --song "Tell Your World" --difficulty EXPERT --score 1023456 --output results.csv
  python pjsekai_result_append.py --interactive --output results.csv
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ResultEntry:
    timestamp: str
    song: str
    difficulty: str
    score: int
    perfect: int
    great: int
    good: int
    bad: int
    miss: int
    max_combo: int
    clear_status: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append a Pjsekai result to a CSV file")
    parser.add_argument("--output", default="pjsekai_results.csv", help="Target CSV path")
    parser.add_argument("--interactive", action="store_true", help="Prompt for all fields")

    parser.add_argument("--song")
    parser.add_argument("--difficulty", choices=["EASY", "NORMAL", "HARD", "EXPERT", "MASTER", "APPEND"])
    parser.add_argument("--score", type=int)
    parser.add_argument("--perfect", type=int)
    parser.add_argument("--great", type=int)
    parser.add_argument("--good", type=int)
    parser.add_argument("--bad", type=int)
    parser.add_argument("--miss", type=int)
    parser.add_argument("--max-combo", dest="max_combo", type=int)
    parser.add_argument("--clear-status", choices=["FAILED", "CLEAR", "FULL COMBO", "ALL PERFECT"])
    return parser.parse_args()


def ask(prompt: str, cast=str):
    while True:
        raw = input(f"{prompt}: ").strip()
        if not raw:
            print("Value cannot be empty.")
            continue
        try:
            return cast(raw)
        except ValueError:
            print("Invalid value. Please try again.")


def build_entry(args: argparse.Namespace) -> ResultEntry:
    if args.interactive:
        song = ask("Song")
        difficulty = ask("Difficulty (EASY/NORMAL/HARD/EXPERT/MASTER/APPEND)").upper()
        score = ask("Score", int)
        perfect = ask("Perfect count", int)
        great = ask("Great count", int)
        good = ask("Good count", int)
        bad = ask("Bad count", int)
        miss = ask("Miss count", int)
        max_combo = ask("Max combo", int)
        clear_status = ask("Clear status (FAILED/CLEAR/FULL COMBO/ALL PERFECT)").upper()
    else:
        required = [
            "song",
            "difficulty",
            "score",
            "perfect",
            "great",
            "good",
            "bad",
            "miss",
            "max_combo",
            "clear_status",
        ]
        missing = [field for field in required if getattr(args, field) is None]
        if missing:
            raise SystemExit(f"Missing required arguments: {', '.join(missing)}")

        song = args.song
        difficulty = args.difficulty
        score = args.score
        perfect = args.perfect
        great = args.great
        good = args.good
        bad = args.bad
        miss = args.miss
        max_combo = args.max_combo
        clear_status = args.clear_status
... 
...     return ResultEntry(
...         timestamp=datetime.now(timezone.utc).isoformat(),
...         song=song,
...         difficulty=difficulty,
...         score=score,
...         perfect=perfect,
...         great=great,
...         good=good,
...         bad=bad,
...         miss=miss,
...         max_combo=max_combo,
...         clear_status=clear_status,
...     )
... 
... 
... def append_row(path: Path, entry: ResultEntry) -> None:
...     path.parent.mkdir(parents=True, exist_ok=True)
...     file_exists = path.exists()
... 
...     with path.open("a", newline="", encoding="utf-8") as csvfile:
...         writer = csv.DictWriter(csvfile, fieldnames=list(ResultEntry.__annotations__.keys()))
...         if not file_exists:
...             writer.writeheader()
...         writer.writerow(entry.__dict__)
... 
... 
... def main() -> None:
...     args = parse_args()
...     entry = build_entry(args)
...     output = Path(args.output)
...     append_row(output, entry)
...     print(f"Appended result for '{entry.song}' ({entry.difficulty}) to {output}")
... 
... 
... if __name__ == "__main__":
...     main()
