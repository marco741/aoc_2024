from collections.abc import Generator
from enum import Enum
from pathlib import Path

type Coord = tuple[int, int]


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


def sum_tuples(t1: Coord, t2: Coord) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def is_valid(matrix: list[list[int]], cell: Coord) -> bool:
    r, c = cell
    return 0 <= r < len(matrix) and 0 <= c < len(matrix[0])


def neighbor(matrix: list[list[int]], cur: Coord) -> Generator[Coord]:
    for direction in (Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT):
        neighbor = sum_tuples(cur, direction.value)
        if is_valid(matrix, neighbor):
            yield neighbor


def load_data(filename: str) -> list[list[int]]:
    text = Path(__file__).parent.joinpath(filename).read_text()

    return [[int(c) for c in line] for line in text.splitlines()]


END_TRAIL = 9
START_TRAIL = 0


def end_score(matrix: list[list[int]], start: Coord) -> int:
    stack: list[Coord] = []
    stack.append(start)
    found = set()
    while len(stack):
        cur = stack.pop()
        if matrix[cur[0]][cur[1]] == END_TRAIL:
            found.add(cur)
        for o in neighbor(matrix, cur):
            if matrix[o[0]][o[1]] == matrix[cur[0]][cur[1]] + 1:
                stack.append(o)
    return len(found)


def trail_score(matrix: list[list[int]], start: Coord) -> int:
    stack: list[Coord] = []
    stack.append(start)
    result = 0
    while len(stack):
        cur = stack.pop()
        if matrix[cur[0]][cur[1]] == END_TRAIL:
            result += 1
        for o in neighbor(matrix, cur):
            if matrix[o[0]][o[1]] == matrix[cur[0]][cur[1]] + 1:
                stack.append(o)
    return result


def trailheads_scores(matrix: list[list[int]]) -> int:
    result = 0
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell != START_TRAIL:
                continue
            result += trail_score(matrix, (r, c))
    return result


def main() -> None:
    matrix = load_data("data.txt")
    print(trailheads_scores(matrix))


if __name__ == "__main__":
    main()
