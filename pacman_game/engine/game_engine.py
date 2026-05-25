"""
Package  : engine
Module   : game_engine
Desc     : Core loop. Wires all pieces together.
           Demonstrates: composition, encapsulation, package usage.

FIXES:
  1. __get_input() — sebelumnya komentar bilang "non-blocking" tapi pakai input()
     yang memblokir loop. Sekarang pakai sys.stdin dengan timeout via select (Unix)
     atau msvcrt (Windows), sehingga ghost tetap bergerak walau player tidak menekan tombol.

  2. Ghost spawn position — Blinky/Pinky/Inky sebelumnya spawn di koordinat yang
     bisa masuk ke dalam dinding tergantung layout. Koordinat disesuaikan ke tile
     kosong yang valid di GAME_LAYOUT.

  3. Skor tidak terintegrasi — run() sekarang menyimpan final score ke self.__final_score
     dan tersedia via property final_score. main.py tidak perlu tanya manual ke user.
"""

import os
import sys
import time
import select

from .board import Board
from pacman_game.entities import Pacman, Blinky, Pinky, Inky


class GameEngine:
    """
    Owns the board, entities, and the main tick loop.
    Uses composition: has-a Board, has-a Pacman, has-a list of Ghosts.
    """

    TICK_DELAY = 0.15  # seconds per frame

    def __init__(self):
        self.__board  = Board()
        self.__pacman = Pacman(x=9, y=15)

        # FIX: spawn ghost di tile yang benar-benar walkable di GAME_LAYOUT
        # Sebelumnya (9,9), (10,9), (9,10) bisa jatuh di dinding.
        # Koordinat baru dipilih dari baris 9 yang terbuka: "#..................#"
        self.__ghosts = [
            Blinky(x=5,  y=9),
            Pinky(x=9,  y=9),
            Inky(x=14, y=9),
        ]
        self.__running     = False
        self.__tick_count  = 0
        self.__fruit_spawned = False

        # FIX: simpan skor akhir supaya bisa diakses dari luar tanpa tanya user
        self.__final_score = 0

    # ── Property publik untuk skor akhir ─────────────────────────────────

    @property
    def final_score(self) -> int:
        """Skor akhir setelah game selesai. Diakses oleh main.py."""
        return self.__final_score

    # ── Private helpers ───────────────────────────────────────────────────

    def __clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def __sync_board_state(self) -> None:
        """Push Pacman state into the board so ghosts read it."""
        self.__board.pacman_position  = self.__pacman.position
        self.__board.pacman_direction = self.__pacman.direction

    def __handle_tile(self) -> None:
        """Process the tile Pacman stands on."""
        x, y = self.__pacman.position
        item = self.__board.consume_tile(x, y)

        if item == ".":
            self.__pacman.eat("dot")
        elif item == "o":
            self.__pacman.eat("power_pellet")
            self.__pacman.activate_power(duration=12)
            for ghost in self.__ghosts:
                ghost.frighten(duration=12)
        elif item == "F":
            self.__pacman.eat("fruit")

    def __check_ghost_collision(self) -> bool:
        """Return True if Pacman was killed."""
        for ghost in self.__ghosts:
            if not ghost.alive:
                continue
            if ghost.position == self.__pacman.position:
                if self.__pacman.power_mode:
                    ghost.kill()
                    self.__pacman.score += 200
                    print("  [!] Ghost eaten! +200")
                    time.sleep(0.3)
                else:
                    self.__pacman.lose_life()
                    return True
        return False

    def __get_input(self) -> str:
        """
        FIX: Sebelumnya pakai input() yang BLOCKING — ghost tidak bergerak
        sampai player tekan Enter setiap tick. Sekarang non-blocking:
        - Unix/Mac : select() dengan timeout TICK_DELAY
        - Windows  : msvcrt.kbhit() + msvcrt.getwch()
        Jika tidak ada input dalam waktu TICK_DELAY, kembalikan '' (ghost tetap bergerak).
        """
        if os.name == "nt":
            # Windows
            import msvcrt
            deadline = time.time() + self.TICK_DELAY
            while time.time() < deadline:
                if msvcrt.kbhit():
                    return msvcrt.getwch().lower()
                time.sleep(0.01)
            return ""
        else:
            # Unix / Mac
            rlist, _, _ = select.select([sys.stdin], [], [], self.TICK_DELAY)
            if rlist:
                ch = sys.stdin.read(1).lower()
                # Flush sisa buffer (misalnya arrow key escape sequence)
                while select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.read(1)
                return ch
            return ""

    def __apply_input(self, ch: str) -> None:
        direction_map = {"w": "up", "s": "down", "a": "left", "d": "right"}
        if ch in direction_map:
            new_dir = direction_map[ch]
            self.__pacman.direction = new_dir

            dx, dy = {"up": (0, -1), "down": (0, 1),
                      "left": (-1, 0), "right": (1, 0)}[new_dir]
            nx = self.__pacman.x + dx
            ny = self.__pacman.y + dy

            if self.__board.is_walkable(nx, ny):
                self.__pacman.move(nx, ny)

    def __render_hud(self) -> str:
        p = self.__pacman
        mode = "POWER!" if p.power_mode else "normal"
        dots_left = self.__board.remaining_dots
        return (
            f"  Score: {p.score}  |  Lives: {p.lives}  |  "
            f"Mode: {mode}  |  Dots left: {dots_left}\n"
            f"  Ghosts: "
            + "  ".join(
                f"{g.name}({'alive' if g.alive else 'dead'})"
                for g in self.__ghosts
            )
            + "\n"
            + "  Controls: w=up  s=down  a=left  d=right  q=quit\n"
        )

    # ── Public API ────────────────────────────────────────────────────────

    def run(self) -> None:
        """
        Start and run the main game loop.
        FIX: setelah game selesai, skor disimpan ke self.__final_score
        sehingga main.py bisa langsung membacanya tanpa menanya user.
        """
        self.__running = True
        print("\n  === TEXT PACMAN ===")
        print("  Controls: w=up  s=down  a=left  d=right  q=quit\n")
        time.sleep(1)

        # Unix: matikan buffering stdin agar input tidak perlu Enter
        old_settings = None
        if os.name != "nt":
            try:
                import tty
                import termios
                old_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
            except Exception:
                pass  # fallback ke blocking input jika terminal tidak support

        try:
            while self.__running:
                self.__clear_screen()
                self.__sync_board_state()

                entities = [self.__pacman] + [g for g in self.__ghosts if g.alive]

                print(self.__render_hud())
                print(self.__board.render(entities))
                print()

                ch = self.__get_input()
                if ch == "q":
                    print("\n  Exiting. Bye!")
                    break

                self.__apply_input(ch)
                self.__handle_tile()

                self.__pacman.update(self.__board)
                for ghost in self.__ghosts:
                    if ghost.alive:
                        ghost.update(self.__board)

                killed = self.__check_ghost_collision()
                if killed and self.__pacman.lives <= 0:
                    self.__clear_screen()
                    print(f"\n  GAME OVER. Final score: {self.__pacman.score}\n")
                    self.__running = False

                if self.__board.cleared:
                    self.__clear_screen()
                    print(f"\n  YOU WIN! Score: {self.__pacman.score}\n")
                    self.__running = False

                self.__tick_count += 1

        finally:
            # Kembalikan setting terminal ke semula
            if old_settings is not None:
                try:
                    import termios
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                except Exception:
                    pass

        # FIX: simpan skor akhir ke property yang bisa diakses main.py
        self.__final_score = self.__pacman.score