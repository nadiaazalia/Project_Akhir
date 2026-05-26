from abc import ABC, abstractmethod


class Entity(ABC):
    """Base class for every object that lives on the game board."""

    def __init__(self, name: str, symbol: str, x: int, y: int):
        # Public
        self.name = name
        self.symbol = symbol

        # Protected (single underscore) — subclasses access these freely
        self._x = x
        self._y = y
        self._alive = True

    # ── Properties (controlled access to protected state) ──────────────

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def position(self) -> tuple:
        return (self._x, self._y)

    @property
    def alive(self) -> bool:
        return self._alive

    # ── Abstract interface every entity must implement ──────────────────

    @abstractmethod
    def update(self, board) -> None:
        """Called once per game tick."""
        pass

    @abstractmethod
    def render(self) -> str:
        """Return the character used to draw this entity."""
        pass

    # ── Shared utility ──────────────────────────────────────────────────

    def kill(self) -> None:
        self._alive = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.name}' at ({self._x},{self._y})>"