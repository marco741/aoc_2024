from collections import Counter
from pathlib import Path


def list_distance(l1: list[int], l2: list[int]) -> int:
    result = 0
    for v1, v2 in zip(sorted(l1), sorted(l2), strict=False):
        result += abs(v1 - v2)
    return result


def similarity(l1: list[int], l2: list[int]) -> int:
    c1 = Counter(l1)
    c2 = Counter(l2)
    result = 0
    for k1, v1 in c1.items():
        if k1 in c2:
            result += k1 * v1 * c2[k1]
    return result


def load_data(filename: str) -> tuple[list[int], list[int]]:
    filepath = Path(__file__).parent.joinpath(filename)
    l1, l2 = [], []
    for line in filepath.read_text().splitlines():
        n1, n2 = line.split()
        l1.append(int(n1))
        l2.append(int(n2))
    return l1, l2


def main() -> None:
    l1, l2 = load_data("data.txt")
    print(list_distance(l1, l2))
    print(similarity(l1, l2))


if __name__ == "__main__":
    main()
