
import sys
import os

# Make sure the project root is on the path
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

    # Save score after game ends
    # (GameEngine exposes final score via pacman — for demo we read from engine)
    # For a full integration, GameEngine would return the score.
    # Here we ask the user.
    try:
        score = int(input("\n  Enter your final score to save it (or 0 to skip): "))
        if score > 0:
            ScoreTracker.add(name, score)
            ScoreTracker.save()
            ScoreTracker.display()
    except ValueError:
        pass


if __name__ == "__main__":
    main()