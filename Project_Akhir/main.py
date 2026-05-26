import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pacman_game.engine import GameEngine
from pacman_game.utils  import ScoreTracker


def main():
    ScoreTracker.load()
    ScoreTracker.display()

    name = input("  Enter your name: ").strip() or "Player"
    print()

    engine = GameEngine()
    engine.run()

    # FIX: baca skor langsung dari engine, tidak perlu tanya user secara manual
    score = engine.final_score
    if score > 0:
        ScoreTracker.add(name, score)
        ScoreTracker.save()
        print(f"\n  Score {score} disimpan untuk {name}!")
        ScoreTracker.display()
    else:
        print("\n  Tidak ada skor yang disimpan.")


if __name__ == "__main__":
    main()