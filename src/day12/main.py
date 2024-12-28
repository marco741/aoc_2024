import itertools
from collections import deque
from enum import Enum
from pathlib import Path
from typing import Literal


def sum_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def multiply_tuple(t: tuple[int, int], n: int) -> tuple[int, int]:
    return t[0] * n, t[1] * n


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)


DIRECTIONS = (Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT)
VERTICAL_DIRECTIONS = (Direction.UP, Direction.DOWN)
HORIZONTAL_DIRECTIONS = (Direction.LEFT, Direction.RIGHT)

type Coord = tuple[int, int]
type Matrix = list[list[str]]
type Orientation = Literal["vertical", "horizontal"]
type Fence = tuple[Coord, Orientation]


def load_data(filename: str) -> Matrix:
    text = Path(__file__).parent.joinpath(filename).read_text()
    return [list(line) for line in text.split()]


def find_cost(matrix: Matrix) -> int:
    n, m = len(matrix), len(matrix[0])
    seen: set[Coord] = set()
    queue: deque[Coord] = deque()
    result = 0
    for coord in itertools.product(range(n), range(m)):
        if coord in seen:
            continue
        area, perimeter = 0, 0
        queue.appendleft(coord)
        seen.add(coord)
        while queue:
            r, c = queue.pop()
            area += 1
            for d in DIRECTIONS:
                r0, c0 = sum_tuples((r, c), d.value)
                if not (0 <= r0 < n and 0 <= c0 < m) or matrix[r0][c0] != matrix[r][c]:
                    perimeter += 1
                elif (r0, c0) not in seen:
                    seen.add((r0, c0))
                    queue.appendleft((r0, c0))
        result += area * perimeter
    return result


def get_sides(fences: set[Fence]) -> int:
    assert len(fences)
    result = 0
    seen: set[Fence] = set()
    for fence in fences:
        if fence in seen:
            continue
        result += 1
        seen.add(fence)
        queue: deque[Fence] = deque()
        queue.appendleft(fence)
        while queue:
            cur, orientation = queue.pop()
            directions = VERTICAL_DIRECTIONS if orientation == "vertical" else HORIZONTAL_DIRECTIONS
            for d in directions:
                neighbor = sum_tuples(cur, multiply_tuple(d.value, 3))
                if (neighbor, orientation) in fences and (neighbor, orientation) not in seen:
                    seen.add((neighbor, orientation))
                    queue.appendleft((neighbor, orientation))

    return result


def find_cost_2(matrix: Matrix) -> int:
    n, m = len(matrix), len(matrix[0])
    seen: set[Coord] = set()
    queue: deque[Coord] = deque()
    result = 0
    for coord in itertools.product(range(n), range(m)):
        if coord in seen:
            continue
        area = 0
        fences: set[Fence] = set()
        queue.appendleft(coord)
        seen.add(coord)
        while queue:
            r, c = queue.pop()
            area += 1
            for d in DIRECTIONS:
                r0, c0 = sum_tuples((r, c), d.value)
                if not (0 <= r0 < n and 0 <= c0 < m) or matrix[r0][c0] != matrix[r][c]:
                    if d in HORIZONTAL_DIRECTIONS:
                        fence_coord: Coord = sum_tuples(multiply_tuple((r, c), 3), d.value)
                        fences.add((fence_coord, "vertical"))
                    else:
                        fence_coord = sum_tuples(multiply_tuple((r, c), 3), d.value)
                        fences.add((fence_coord, "horizontal"))
                elif (r0, c0) not in seen:
                    seen.add((r0, c0))
                    queue.appendleft((r0, c0))

        sides = get_sides(fences)
        print(matrix[coord[0]][coord[1]], area, sides)
        result += area * sides
    return result


def main() -> None:
    matrix = load_data("data.txt")
    cost = find_cost_2(matrix)
    print(cost)


if __name__ == "__main__":
    main()
