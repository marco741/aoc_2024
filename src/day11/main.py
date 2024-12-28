import sys
from functools import cache
from pathlib import Path

sys.setrecursionlimit(1000000000)


def transform_stone(stone: int) -> tuple[int, ...]:
    if stone == 0:
        return (1,)
    if len(digits := str(stone)) % 2 == 0:
        return int(digits[: len(digits) // 2]), int(digits[len(digits) // 2 :])
    return (stone * 2024,)


@cache
def blink(stone: int, n: int) -> int:
    if n == 0:
        return 1

    stones = transform_stone(stone)
    return sum(blink(s, n - 1) for s in stones)


def count(stones: list[int], n: int) -> int:
    result = 0
    for s in stones:
        result += blink(s, n)
    return result


def load_data(filename: str) -> list[int]:
    text = Path(__file__).parent.joinpath(filename).read_text()
    return [int(c) for c in text.split()]


def main() -> None:
    stones = load_data("data.txt")
    print(count(stones, 1000))


if __name__ == "__main__":
    main()
