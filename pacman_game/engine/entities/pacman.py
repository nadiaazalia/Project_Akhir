"""
Package  : entities
Module   : pacman
Desc     : Pacman player entity.
           Demonstrates: inheritance, encapsulation, method override.
"""

from .base_entity import Entity


class Pacman(Entity):
    """The player-controlled character."""

    SYMBOLS = {
        "right": "C",
        "left":  "Ↄ",
        "up":    "v",
        "down":  "^",
        "mouth_closed": "O",
    }

    def __init__(self, x: int, y: int):
        super().__init__(name="Pacman", symbol="C", x=x, y=y)

        # Public
        self.score = 0
        self.lives = 3

        # Protected
        self._direction = "right"
        self._power_mode = False
        self._power_ticks = 0

        # Private (double underscore — name-mangled, truly internal)
        self.__mouth_open = True
        self.__tick_count = 0

    # ── Properties ──────────────────────────────────────────────────────

    @property
    def direction(self) -> str:
        return self._direction

    @direction.setter
    def direction(self, value: str) -> None:
        valid = {"up", "down", "left", "right"}
        if value not in valid:
            raise ValueError(f"Direction must be one of {valid}")
        self._direction = value

    @property
    def power_mode(self) -> bool:
        return self._power_mode

    # ── Private helpers ──────────────────────────────────────────────────

    def __toggle_mouth(self) -> None:
        """Animate mouth — only this class touches this."""
        self.__mouth_open = not self.__mouth_open

    def __decay_power(self) -> None:
        """Count down power pellet timer."""
        if self._power_mode:
            self._power_ticks -= 1
            if self._power_ticks <= 0:
                self._power_mode = False

    # ── Public interface ─────────────────────────────────────────────────

    def activate_power(self, duration: int = 10) -> None:
        self._power_mode = True
        self._power_ticks = duration
        print("  [!] POWER MODE ACTIVATED!")

    def eat(self, item_type: str) -> int:
        """Eat a tile and return points earned."""
        points = {"dot": 10, "power_pellet": 50, "fruit": 100}.get(item_type, 0)
        self.score += points
        return points

    def lose_life(self) -> None:
        self.lives -= 1
        self._direction = "right"
        print(f"  [!] Lives remaining: {self.lives}")

    def move(self, nx: int, ny: int) -> None:
        """Move to new coordinates."""
        self._x = nx
        self._y = ny

    # ── Entity interface ─────────────────────────────────────────────────

    def update(self, board) -> None:
        self.__tick_count += 1
        if self.__tick_count % 2 == 0:
            self.__toggle_mouth()
        self.__decay_power()

    def render(self) -> str:
        if not self.__mouth_open:
            return self.SYMBOLS["mouth_closed"]
        if self._power_mode:
            return "@"
        return self.SYMBOLS.get(self._direction, "C")