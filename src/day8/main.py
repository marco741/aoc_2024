import itertools
from collections import defaultdict
from pathlib import Path


def in_matrix(coords: tuple[int, int], matrix: list[list[str]]) -> bool:
    rows, cols = len(matrix), len(matrix[0])
    r, c = coords
    return 0 <= r < rows and 0 <= c < cols


def count_hotspots(matrix: list[list[str]]) -> int:
    location_map: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell != ".":
                location_map[cell].append((r, c))
    hotspots: set[tuple[int, int]] = set()
    for antennas in location_map.values():
        for a1, a2 in itertools.combinations(antennas, 2):
            hs: tuple[int, int] = tuple(map(lambda x1, x2: 2 * x2 - x1, a1, a2))
            if in_matrix(hs, matrix):
                hotspots.add(hs)
            hs: tuple[int, int] = tuple(map(lambda x1, x2: 2 * x1 - x2, a1, a2))
            if in_matrix(hs, matrix):
                hotspots.add(hs)

    return len(hotspots)


def sum_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] + t2[0], t1[1] + t2[1]


def sub_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    return t1[0] - t2[0], t1[1] - t2[1]


def count_more_hotspots(matrix: list[list[str]]) -> int:
    location_map: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell != ".":
                location_map[cell].append((r, c))
    hotspots: set[tuple[int, int]] = set()
    for antennas in location_map.values():
        for c1, c2 in itertools.combinations(antennas, 2):
            dist = sub_tuples(c2, c1)

            while in_matrix(c1, matrix):
                hotspots.add(c1)
                c1 = sub_tuples(c1, dist)

            while in_matrix(c2, matrix):
                hotspots.add(c2)
                c2 = sum_tuples(c2, dist)

    return len(hotspots)


def load_data(filename: str) -> list[list[str]]:
    text = Path(__file__).parent.joinpath(filename).read_text()
    return [list(line) for line in text.splitlines()]


def main() -> None:
    matrix = load_data("data.txt")
    print(count_more_hotspots(matrix))


if __name__ == "__main__":
    main()
