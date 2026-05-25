"""
Package  : utils
Module   : score_tracker
Desc     : High score management.
           Demonstrates: class methods, static methods, encapsulation.
"""

import json
import os


class ScoreEntry:
    """Immutable record of a single game result."""

    def __init__(self, player: str, score: int):
        self.__player = player
        self.__score  = score

    @property
    def player(self) -> str:
        return self.__player

    @property
    def score(self) -> int:
        return self.__score

    def to_dict(self) -> dict:
        return {"player": self.__player, "score": self.__score}

    def __repr__(self) -> str:
        return f"{self.__player}: {self.__score}"


class ScoreTracker:
    """
    Manages high scores.
    Uses class-level state and class/static methods.
    """

    _FILE = "scores.json"
    _entries: list[ScoreEntry] = []  # Class variable shared by all instances

    @classmethod
    def load(cls) -> None:
        """Load scores from disk into the class-level list."""
        if os.path.exists(cls._FILE):
            with open(cls._FILE, "r") as f:
                data = json.load(f)
                cls._entries = [ScoreEntry(d["player"], d["score"]) for d in data]

    @classmethod
    def save(cls) -> None:
        """Persist current scores to disk."""
        with open(cls._FILE, "w") as f:
            json.dump([e.to_dict() for e in cls._entries], f, indent=2)

    @classmethod
    def add(cls, player: str, score: int) -> None:
        cls._entries.append(ScoreEntry(player, score))
        cls._entries.sort(key=lambda e: e.score, reverse=True)
        cls._entries = cls._entries[:10]  # Keep top 10

    @classmethod
    def top(cls, n: int = 5) -> list:
        return cls._entries[:n]

    @staticmethod
    def format_entry(rank: int, entry: ScoreEntry) -> str:
        """Pure formatting util; needs no class or instance state."""
        return f"  {rank:>2}. {entry.player:<15} {entry.score:>6} pts"

    @classmethod
    def display(cls) -> None:
        print("\n  === HIGH SCORES ===")
        for i, entry in enumerate(cls.top(), start=1):
            print(cls.format_entry(i, entry))
        print()