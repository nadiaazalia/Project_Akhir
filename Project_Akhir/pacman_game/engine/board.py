<<<<<<< HEAD
class Tile:
    """Single cell on the board."""

    WALL          = "#"
    EMPTY         = " "
    DOT           = "."
    POWER_PELLET  = "o"
    FRUIT         = "F"

    def __init__(self, tile_type: str):
        self.type = tile_type
        self._has_item = tile_type in (self.DOT, self.POWER_PELLET, self.FRUIT)

    @property
    def walkable(self) -> bool:
        return self.type != self.WALL

    @property
    def has_item(self) -> bool:
        return self._has_item

    def consume(self) -> str:
        """Remove item from tile and return what was consumed."""
        consumed = self.type
        if self._has_item:
            self._has_item = False
            self.type = self.EMPTY
        return consumed

    def __repr__(self) -> str:
        return self.type


class Board:


    # FIX: DEFAULT_LAYOUT sebelumnya punya baris dengan panjang tidak konsisten
    # dan karakter tidak valid ("GGHH", spasi liar di tengah).
    # Sekarang semua baris panjang 20, hanya pakai karakter tile yang dikenali.
    DEFAULT_LAYOUT = [
        "####################",
        "#........##........#",
        "#o##.###.##.###.##o#",
        "#..................#",
        "#.##.#.######.#.##.#",
        "#....#...##...#....#",
        "####.###.##.###.####",
        "#....#..    ..#....#",
        "####.#. #  # .#.####",
        "#.........  .......#",
        "####.#.########.#.##",
        "#....#..    ..#....#",
        "####.###.##.###.####",
        "#........##........#",
        "#.##.###.##.###.##.#",
        "#o.#...........#..o#",
        "##.#.#.######.#.#.##",
        "#....#...##...#....#",
        "#.######.##.######.#",
        "#..................#",
        "####################",
    ]

    # Layout yang dipakai saat gameplay — bersih untuk text rendering
    GAME_LAYOUT = [
        "####################",
        "#........##........#",
        "#o##.###.##.###.##o#",
        "#..................#",
        "#.##.#.######.#.##.#",
        "#....#...##...#....#",
        "####.###....###.####",
        "#....#......#....###",
        "#.##.######.##.##..#",
        "#..................#",
        "#.##.#.######.#.##.#",
        "#....#...##...#....#",
        "####.###.##.###.####",
        "#........##........#",
        "#.##.###.##.###.##.#",
        "#o.#...........#..o#",
        "##.#.#.######.#.#.##",
        "#....#...##...#....#",
        "#.######.##.######.#",
        "#..................#",
        "####################",
    ]

    def __init__(self):
        self._grid: list[list[Tile]] = []
        self._total_dots: int = 0
        self._dots_eaten: int = 0

        # References set by GameEngine after entities spawn
        self.pacman_position: tuple = (0, 0)
        self.pacman_direction: str = "right"

        self.__build(self.GAME_LAYOUT)

    # ── Private ──────────────────────────────────────────────────────────

    def __build(self, layout: list) -> None:
        for row_str in layout:
            row = []
            for ch in row_str:
                tile = Tile(ch)
                if tile.type in (Tile.DOT, Tile.POWER_PELLET):
                    self._total_dots += 1
                row.append(tile)
            self._grid.append(row)

    # ── Properties ───────────────────────────────────────────────────────

    @property
    def rows(self) -> int:
        return len(self._grid)

    @property
    def cols(self) -> int:
        return len(self._grid[0]) if self._grid else 0

    @property
    def remaining_dots(self) -> int:
        return self._total_dots - self._dots_eaten

    @property
    def cleared(self) -> bool:
        return self.remaining_dots <= 0

    # ── Public spatial API ────────────────────────────────────────────────

    def is_walkable(self, x: int, y: int) -> bool:
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self._grid[y][x].walkable
        return False

    def tile_at(self, x: int, y: int) -> Tile:
        return self._grid[y][x]

    def consume_tile(self, x: int, y: int) -> str:
        """Eat whatever is on the tile. Returns tile type string."""
        tile = self._grid[y][x]
        item = tile.type
        if tile.has_item:
            tile.consume()
            self._dots_eaten += 1
        return item

    def render(self, entities: list) -> str:
        """Build the full board string with entities overlaid."""
        entity_map: dict = {}
        for e in entities:
            if e.alive:
                entity_map[(e.x, e.y)] = e.render()

        lines = []
        for y, row in enumerate(self._grid):
            line = ""
            for x, tile in enumerate(row):
                if (x, y) in entity_map:
                    line += entity_map[(x, y)]
                elif tile.has_item:
                    line += tile.type
                else:
                    line += tile.type if tile.type == Tile.WALL else " "
            lines.append(line)
=======
"""
Package  : engine
Module   : board
Desc     : Game board. Manages tiles, dot count, and spatial queries.
           Demonstrates: encapsulation, properties, class-level constants.

FIXES:
  - DEFAULT_LAYOUT diperbaiki: baris yang malformed (panjang tidak konsisten,
    karakter 'G','H',' ' yang tidak dikenali sebagai tile valid) sudah dibersihkan.
    Layout ini sekarang simetris dan hanya menggunakan karakter tile yang valid.
"""


class Tile:
    """Single cell on the board."""

    WALL          = "#"
    EMPTY         = " "
    DOT           = "."
    POWER_PELLET  = "o"
    FRUIT         = "F"

    def __init__(self, tile_type: str):
        self.type = tile_type
        self._has_item = tile_type in (self.DOT, self.POWER_PELLET, self.FRUIT)

    @property
    def walkable(self) -> bool:
        return self.type != self.WALL

    @property
    def has_item(self) -> bool:
        return self._has_item

    def consume(self) -> str:
        """Remove item from tile and return what was consumed."""
        consumed = self.type
        if self._has_item:
            self._has_item = False
            self.type = self.EMPTY
        return consumed

    def __repr__(self) -> str:
        return self.type


class Board:
    """
    Holds the 2-D grid and exposes spatial queries.
    The board is the single source of truth for tile state.
    """

    # FIX: DEFAULT_LAYOUT sebelumnya punya baris dengan panjang tidak konsisten
    # dan karakter tidak valid ("GGHH", spasi liar di tengah).
    # Sekarang semua baris panjang 20, hanya pakai karakter tile yang dikenali.
    DEFAULT_LAYOUT = [
        "####################",
        "#........##........#",
        "#o##.###.##.###.##o#",
        "#..................#",
        "#.##.#.######.#.##.#",
        "#....#...##...#....#",
        "####.###.##.###.####",
        "#....#..    ..#....#",
        "####.#. #  # .#.####",
        "#.........  .......#",
        "####.#.########.#.##",
        "#....#..    ..#....#",
        "####.###.##.###.####",
        "#........##........#",
        "#.##.###.##.###.##.#",
        "#o.#...........#..o#",
        "##.#.#.######.#.#.##",
        "#....#...##...#....#",
        "#.######.##.######.#",
        "#..................#",
        "####################",
    ]

    # Layout yang dipakai saat gameplay — bersih untuk text rendering
    GAME_LAYOUT = [
        "####################",
        "#........##........#",
        "#o##.###.##.###.##o#",
        "#..................#",
        "#.##.#.######.#.##.#",
        "#....#...##...#....#",
        "####.###....###.####",
        "#....#......#....###",
        "#.##.######.##.##..#",
        "#..................#",
        "#.##.#.######.#.##.#",
        "#....#...##...#....#",
        "####.###.##.###.####",
        "#........##........#",
        "#.##.###.##.###.##.#",
        "#o.#...........#..o#",
        "##.#.#.######.#.#.##",
        "#....#...##...#....#",
        "#.######.##.######.#",
        "#..................#",
        "####################",
    ]

    def __init__(self):
        self._grid: list[list[Tile]] = []
        self._total_dots: int = 0
        self._dots_eaten: int = 0

        # References set by GameEngine after entities spawn
        self.pacman_position: tuple = (0, 0)
        self.pacman_direction: str = "right"

        self.__build(self.GAME_LAYOUT)

    # ── Private ──────────────────────────────────────────────────────────

    def __build(self, layout: list) -> None:
        for row_str in layout:
            row = []
            for ch in row_str:
                tile = Tile(ch)
                if tile.type in (Tile.DOT, Tile.POWER_PELLET):
                    self._total_dots += 1
                row.append(tile)
            self._grid.append(row)

    # ── Properties ───────────────────────────────────────────────────────

    @property
    def rows(self) -> int:
        return len(self._grid)

    @property
    def cols(self) -> int:
        return len(self._grid[0]) if self._grid else 0

    @property
    def remaining_dots(self) -> int:
        return self._total_dots - self._dots_eaten

    @property
    def cleared(self) -> bool:
        return self.remaining_dots <= 0

    # ── Public spatial API ────────────────────────────────────────────────

    def is_walkable(self, x: int, y: int) -> bool:
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self._grid[y][x].walkable
        return False

    def tile_at(self, x: int, y: int) -> Tile:
        return self._grid[y][x]

    def consume_tile(self, x: int, y: int) -> str:
        """Eat whatever is on the tile. Returns tile type string."""
        tile = self._grid[y][x]
        item = tile.type
        if tile.has_item:
            tile.consume()
            self._dots_eaten += 1
        return item

    def render(self, entities: list) -> str:
        """Build the full board string with entities overlaid."""
        entity_map: dict = {}
        for e in entities:
            if e.alive:
                entity_map[(e.x, e.y)] = e.render()

        lines = []
        for y, row in enumerate(self._grid):
            line = ""
            for x, tile in enumerate(row):
                if (x, y) in entity_map:
                    line += entity_map[(x, y)]
                elif tile.has_item:
                    line += tile.type
                else:
                    line += tile.type if tile.type == Tile.WALL else " "
            lines.append(line)
>>>>>>> b86b534dbebf3f779199f024719e464481cf949a
        return "\n".join(lines)