import itertools
from pathlib import Path


def is_valid(report: str) -> bool:
    all_increasing = all((s - f) > 0 for f, s in itertools.pairwise(report))
    all_decreasing = all((s - f) < 0 for f, s in itertools.pairwise(report))
    all_close = all(abs(s - f) <= 3 for f, s in itertools.pairwise(report))

    return (all_increasing or all_decreasing) and all_close


def count_dampener_safe(data: list[list[int]]) -> int:
    result = 0
    for report in data:
        if len(report) <= 1:
            result += 1
            continue

        if is_valid(report) or any(
            is_valid(report[:i] + report[i + 1 :]) for i in range(len(report))
        ):
            result += 1

    return result


def count_safe(data: list[list[int]]) -> int:
    result = 0
    for report in data:
        if len(report) <= 1:
            result += 1
            continue
        all_increasing = all((s - f) > 0 for f, s in itertools.pairwise(report))
        all_decreasing = all((s - f) < 0 for f, s in itertools.pairwise(report))
        all_close = all(abs(s - f) <= 3 for f, s in itertools.pairwise(report))

        if (all_increasing or all_decreasing) and all_close:
            result += 1

    return result


def load_data(filename: str) -> list[list[int]]:
    filepath = Path(__file__).parent.joinpath(filename)
    result: list[list[int]] = []

    for line in filepath.read_text().splitlines():
        result.append([int(v) for v in line.split()])
    return result


def main() -> None:
    filename = "data.txt"
    data = load_data(filename)
    print(count_dampener_safe(data))


if __name__ == "__main__":
    main()
