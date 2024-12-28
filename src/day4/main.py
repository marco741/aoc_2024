import operator
from collections import Counter
from pathlib import Path

DIRECTIONS: tuple[tuple[int, int], ...] = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
)
DIRECTIONS_MS: tuple[tuple[int, int], ...] = (
    (1, 1),
    (1, -1),
    (-1, -1),
    (-1, 1),
)
TARGET = "XMAS"
TARGET_MS = Counter(["M", "M", "M", "M", "S", "S", "S", "S"])


def is_valid(cell: tuple[int, int], lines: list[str]) -> bool:
    return 0 <= cell[0] < len(lines) and 0 <= cell[1] < len(lines[0])


def neighbor_words(cell: tuple[int, int], lines: list[str]) -> int:
    result = 0
    for direction in DIRECTIONS:
        r, c = map(operator.add, cell, direction)
        i = 1
        while is_valid((r, c), lines) and lines[r][c] == TARGET[i]:
            i += 1
            if i == len(TARGET):
                result += 1
                break
            r, c = map(operator.add, (r, c), direction)
    return result


def find_xmas(lines: list[str]) -> int:
    result = 0
    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell != "X":
                continue
            result += neighbor_words((i, j), lines)

    return result


def neighbor_words_mas(cell: tuple[int, int], lines: list[str]) -> int:
    found: Counter[str] = Counter()
    for direction in DIRECTIONS_MS:
        r, c = map(operator.add, cell, direction)
        if not is_valid((r, c), lines):
            return 0
        found[lines[r][c]] += 1 + (abs(sum(direction)))
    return int(found == TARGET_MS)


def find_mas(lines: list[str]) -> int:
    result = 0
    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell != "A":
                continue
            result += neighbor_words_mas((i, j), lines)

    return result


def load_data(filename: str) -> list[str]:
    filepath = Path(__file__).parent.joinpath(filename)

    return filepath.read_text().splitlines()


def main() -> None:
    filename = "data.txt"
    lines = load_data(filename)
    print(find_mas(lines))


if __name__ == "__main__":
    main()
