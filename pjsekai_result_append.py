#!/usr/bin/env python3
"""Append Project Sekai result entries to a JSONL file.

Usage examples:
  python pjsekai_result_append.py --song "Tell Your World" --difficulty EXPERT --score 1023456 --output results.jsonl
  python pjsekai_result_append.py --interactive --output results.jsonl
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

DIFFICULTIES = ["EASY", "NORMAL", "HARD", "EXPERT", "MASTER", "APPEND"]
CLEAR_STATUSES = ["FAILED", "CLEAR", "FULL COMBO", "ALL PERFECT"]


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
    parser = argparse.ArgumentParser(description="Append a Pjsekai result to a JSONL file")
    parser.add_argument("--output", default="pjsekai_results.jsonl", help="Target JSONL path")
    parser.add_argument("--interactive", action="store_true", help="Prompt for all fields")

    parser.add_argument("--song")
    parser.add_argument("--difficulty", choices=DIFFICULTIES)
    parser.add_argument("--score", type=int)
    parser.add_argument("--perfect", type=int)
    parser.add_argument("--great", type=int)
    parser.add_argument("--good", type=int)
    parser.add_argument("--bad", type=int)
    parser.add_argument("--miss", type=int)
    parser.add_argument("--max-combo", dest="max_combo", type=int)
    parser.add_argument("--clear-status", choices=CLEAR_STATUSES)
    return parser.parse_args()


def ask_text(prompt: str) -> str:
    while True:
        value = input(f"{prompt}: ").strip()
        if value:
            return value
        print("Value cannot be empty.")


def ask_int(prompt: str) -> int:
    while True:
        raw = input(f"{prompt}: ").strip()
        try:
            value = int(raw)
        except ValueError:
            print("Invalid number. Please enter an integer.")
            continue
        if value < 0:
            print("Value cannot be negative.")
            continue
        return value


def ask_choice(prompt: str, options: list[str]) -> str:
    option_text = "/".join(options)
    while True:
        value = input(f"{prompt} ({option_text}): ").strip().upper()
        if value in options:
            return value
        print("Invalid option. Please choose one of the listed values.")


def build_entry(args: argparse.Namespace) -> ResultEntry:
    if args.interactive:
        song = ask_text("Song")
        difficulty = ask_choice("Difficulty", DIFFICULTIES)
        score = ask_int("Score")
        perfect = ask_int("Perfect count")
        great = ask_int("Great count")
        good = ask_int("Good count")
        bad = ask_int("Bad count")
        miss = ask_int("Miss count")
        max_combo = ask_int("Max combo")
        clear_status = ask_choice("Clear status", CLEAR_STATUSES)
    else:
        required = (
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
        )
        missing = [name for name in required if getattr(args, name) is None]
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

    return ResultEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        song=song,
        difficulty=difficulty,
        score=score,
        perfect=perfect,
        great=great,
        good=good,
        bad=bad,
        miss=miss,
        max_combo=max_combo,
        clear_status=clear_status,
    )


def append_entry(path: Path, entry: ResultEntry) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as outfile:
        outfile.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")


def main() -> None:
    args = parse_args()
    entry = build_entry(args)
    output = Path(args.output)
    append_entry(output, entry)
    print(f"Appended result for '{entry.song}' ({entry.difficulty}) to {output}")


if __name__ == "__main__":
    main()
