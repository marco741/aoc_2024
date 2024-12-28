import operator
from enum import Enum
from pathlib import Path


def find_start(matrix: list[list[str]]) -> tuple[int, int] | None:
    for r, line in enumerate(matrix):
        for c, cell in enumerate(line):
            if cell == "^":
                return r, c
    return None


class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    def succ(self) -> "Direction":
        match self:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP
        raise ValueError

    def char(self) -> str:
        match self:
            case Direction.UP:
                return "↑"
            case Direction.RIGHT:
                return "→"
            case Direction.DOWN:
                return "↓"
            case Direction.LEFT:
                return "←"
        raise ValueError


def sum_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return tuple(map(operator.add, t1, t2))


def get_cell(matrix: list[list[str]], cell: tuple[int, int]) -> str | None:
    r, c = cell
    if 0 <= r < len(matrix) and 0 <= c < len(matrix[0]):
        return matrix[r][c]
    return None


def check_visited_positions(matrix: list[list[str]]) -> int | None:
    seen = set()

    cur: tuple[int, int] | None = find_start(matrix)
    if cur is None:
        return None

    direction = Direction.UP

    while True:
        seen.add(cur)
        matrix[cur[0]][cur[1]] = "X"

        while True:
            next = sum_tuples(cur, direction.value)
            cell = get_cell(matrix, next)
            if cell is None:
                return len(seen)
            if cell != "#":
                break
            direction = direction.succ()
        cur = next


def is_loop(
    matrix: list[list[str]], cur: tuple[int, int], direction: Direction, block: tuple[int, int]
) -> bool:
    seen: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    while True:
        if (cur, direction.value) in seen:
            return True

        while True:
            next = sum_tuples(cur, direction.value)
            cell = get_cell(matrix, next)
            if cell is None:
                return False
            if cell == "#" or next == block:
                seen.add((cur, direction.value))
                direction = direction.succ()
            else:
                break
        cur = next


def loops(matrix: list[list[str]]) -> int:
    start: tuple[int, int] | None = find_start(matrix)
    if start is None:
        raise Exception

    direction = Direction.UP

    tmp = "0"

    result: set[tuple[int, int]] = set()
    seen = set()

    cur = start
    while True:
        seen.add(cur)
        next = sum_tuples(cur, direction.value)
        cell = get_cell(matrix, next)

        if cell is None:
            return len(result)
        if cell == "#":
            direction = direction.succ()
            continue
        if next not in result | seen:
            matrix[next[0]][next[1]], tmp = tmp, matrix[next[0]][next[1]]
            if is_loop(matrix, start, Direction.UP, next):
                result.add(next)
                print("-", end="", flush=True)
            matrix[next[0]][next[1]], tmp = tmp, matrix[next[0]][next[1]]

        cur = next


def load_data(filename: str) -> list[list[str]]:
    filepath = Path(__file__).parent.joinpath(filename)

    matrix = [list(line) for line in filepath.read_text().splitlines()]
    return matrix


def main() -> None:
    matrix = load_data("data2.txt")
    print(loops(matrix))


if __name__ == "__main__":
    main()
