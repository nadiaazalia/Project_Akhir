import random
from abc import abstractmethod
from .base_entity import Entity


# ── Level 1 inheritance: Ghost ← Entity ────────────────────────────────────

class Ghost(Entity):
    """Base ghost. Handles shared movement logic and state."""

    FRIGHTENED_SYMBOL = "F"

    def __init__(self, name: str, symbol: str, x: int, y: int, color_tag: str):
        super().__init__(name=name, symbol=symbol, x=x, y=y)

        # Protected
        self._color_tag = color_tag
        self._frightened = False
        self._frightened_ticks = 0

        # Private
        self.__move_counter = 0

    # ── Properties ──────────────────────────────────────────────────────

    @property
    def frightened(self) -> bool:
        return self._frightened

    # ── Public interface ─────────────────────────────────────────────────

    def frighten(self, duration: int = 10) -> None:
        self._frightened = True
        self._frightened_ticks = duration

    def get_valid_moves(self, board) -> list:
        """Return list of (nx, ny) positions the ghost can physically reach."""
        moves = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = self._x + dx, self._y + dy
            if board.is_walkable(nx, ny):
                moves.append((nx, ny))
        return moves

    # ── Private ──────────────────────────────────────────────────────────

    def __decay_frighten(self) -> None:
        if self._frightened:
            self._frightened_ticks -= 1
            if self._frightened_ticks <= 0:
                self._frightened = False

    # ── Abstract method subclasses MUST override ──────────────────────────
    # FIX: sebelumnya hanya raise NotImplementedError biasa, bukan @abstractmethod
    # Akibatnya subclass yang lupa override baru error saat runtime, bukan saat instantiasi.

    @abstractmethod
    def choose_move(self, board, pacman_pos: tuple) -> tuple:
        """Each ghost picks moves differently. Must be overridden."""
        pass

    # ── Entity interface ─────────────────────────────────────────────────

    def update(self, board) -> None:
        self.__decay_frighten()
        self.__move_counter += 1

        if self._frightened:
            # Frightened ghosts move randomly every 2 ticks
            if self.__move_counter % 2 == 0:
                moves = self.get_valid_moves(board)
                if moves:
                    self._x, self._y = random.choice(moves)
        else:
            # FIX: sebelumnya `% 1 == 0` yang SELALU True setiap tick.
            # Sekarang ghost normal bergerak setiap 2 tick — lebih fair untuk player.
            if self.__move_counter % 2 == 0:
                moves = self.get_valid_moves(board)
                if moves:
                    nx, ny = self.choose_move(board, board.pacman_position)
                    self._x, self._y = nx, ny

    def render(self) -> str:
        if self._frightened:
            return self.FRIGHTENED_SYMBOL
        return self.symbol


# ── Level 2 inheritance: concrete ghosts ────────────────────────────────────

class Blinky(Ghost):
    """
    Red ghost. Chases Pacman directly.
    Strategy: always move toward Pacman's current tile.
    """

    def __init__(self, x: int, y: int):
        super().__init__(name="Blinky", symbol="B", x=x, y=y, color_tag="RED")

    def choose_move(self, board, pacman_pos: tuple) -> tuple:
        moves = self.get_valid_moves(board)
        if not moves:
            return (self._x, self._y)

        px, py = pacman_pos
        best = min(moves, key=lambda pos: abs(pos[0] - px) + abs(pos[1] - py))
        return best


class Pinky(Ghost):
    """
    Pink ghost. Targets 2 tiles ahead of Pacman's direction.
    Strategy: ambush by leading the target.
    """

    def __init__(self, x: int, y: int):
        super().__init__(name="Pinky", symbol="P", x=x, y=y, color_tag="PINK")

        # Protected attribute unique to Pinky
        self._lead_tiles = 2

    def choose_move(self, board, pacman_pos: tuple) -> tuple:
        moves = self.get_valid_moves(board)
        if not moves:
            return (self._x, self._y)

        px, py = pacman_pos
        direction = board.pacman_direction

        offsets = {
            "right": (self._lead_tiles, 0),
            "left":  (-self._lead_tiles, 0),
            "up":    (0, -self._lead_tiles),
            "down":  (0, self._lead_tiles),
        }
        dx, dy = offsets.get(direction, (0, 0))
        tx, ty = px + dx, py + dy

        best = min(moves, key=lambda pos: abs(pos[0] - tx) + abs(pos[1] - ty))
        return best


class Inky(Ghost):
    """
    Cyan ghost. Moves randomly with a slight bias toward Pacman.
    Strategy: unpredictable, harder to dodge.
    """

    def __init__(self, x: int, y: int):
        super().__init__(name="Inky", symbol="I", x=x, y=y, color_tag="CYAN")

    def choose_move(self, board, pacman_pos: tuple) -> tuple:
        moves = self.get_valid_moves(board)
        if not moves:
            return (self._x, self._y)

        # 60% chance to move toward Pacman, 40% random
        if random.random() < 0.6:
            px, py = pacman_pos
            return min(moves, key=lambda pos: abs(pos[0] - px) + abs(pos[1] - py))
        return random.choice(moves)