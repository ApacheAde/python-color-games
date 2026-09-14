#!/usr/bin/env python3
"""Tiny launcher for the color games collection."""  # noqa: EXE001
import os
import subprocess
import sys

GAMES = [
    ("1", "Pipe Jumper (platformer)", "pipe_jumper.py"),
    ("2", "Neon Blackjack (cards)", "neon_blackjack.py"),
    ("3", "Lucky Reels (slots)", "lucky_reels.py"),
    ("4", "Color Wheel (roulette)", "color_wheel.py"),
    ("5", "Memory Flip (matching)", "memory_flip.py"),
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    print("\n  PYTHON COLOR GAMES")
    print("  https://x.com/ElbowOS\n")
    for key, label, _ in GAMES:
        print(f"  [{key}] {label}")
    print("  [q] quit\n")
    choice = input("  pick a game: ").strip().lower()
    if choice in ("q", "quit", ""):
        return
    for key, _, filename in GAMES:
        if choice == key:
            path = os.path.join(here, filename)
            subprocess.call([sys.executable, path])
            return
    print("  unknown choice")


if __name__ == "__main__":
    main()
