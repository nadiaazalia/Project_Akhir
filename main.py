"""
main.py — Entry point for Text Pacman.

Run with:
    python main.py

OOP concepts demonstrated in this project:
  - Abstraction      : Entity (ABC) defines the interface all actors follow
  - Encapsulation    : Private (__), protected (_), public attributes across all classes
  - Inheritance      : Ghost <- Entity, Blinky/Pinky/Inky <- Ghost (multi-level)
  - Polymorphism     : board.render() calls e.render() on any Entity subtype
  - Composition      : GameEngine has-a Board, has-a Pacman, has-a list[Ghost]
  - Class methods    : ScoreTracker.load(), .save(), .add()
  - Static methods   : ScoreTracker.format_entry()
  - Properties       : Controlled access to protected state throughout
  - Abstract methods : Entity.update(), Entity.render()
  - Packages         : entities, engine, utils with proper __init__.py exports
"""

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
