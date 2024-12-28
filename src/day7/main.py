from dataclasses import dataclass
from pathlib import Path


@dataclass
class Equation:
    result: int
    numbers: list[int]


def is_correct_rec(numbers: list[int], result: float, i: int) -> bool:
    if i < 0:
        return result == 0
    if int(result) != result:
        return False
    corrects = []
    corrects.append(is_correct_rec(numbers, result - numbers[i], i - 1))
    corrects.append(is_correct_rec(numbers, result / numbers[i], i - 1))
    return any(corrects)


def is_correct_3(numbers: list[int], result: float, i: int) -> bool:
    if i < 0:
        return result == 0
    if result < 0 or int(result) != result:
        return False
    result = int(result)

    num = numbers[i]
    corrects = []
    if str(result).endswith(str(num)):
        corrects.append(is_correct_3(numbers, int(("0" + str(result))[: -len(str(num))]), i - 1))
    corrects.append(is_correct_3(numbers, result - int(num), i - 1))
    corrects.append(is_correct_3(numbers, result / int(num), i - 1))
    return any(corrects)


def is_correct_dp(arr: list[int], result: int) -> bool:
    if arr[0] > result:
        return False

    prev = [False] * (result + 1)
    prev[arr[0]] = True
    for i in range(1, len(arr)):
        cur = [False] * (result + 1)
        for j, ok in enumerate(prev):
            if not ok:
                continue

            values = [j + arr[i], j * arr[i], int(f"{j}{arr[i]}")]
            for val in values:
                if val < len(cur):
                    cur[val] = True

        prev = cur

    return prev[-1]


def is_correct_set(arr: list[int], result: int) -> bool:
    if arr[0] > result:
        return False

    prev: set[int] = set()
    prev.add(arr[0])
    for i in range(1, len(arr)):
        cur: set[int] = set()
        for j in prev:
            values = [j + arr[i], j * arr[i], int(f"{j}{arr[i]}")]
            for val in values:
                if val <= result:
                    cur.add(val)

        prev = cur

    return result in prev


# numbers = [3, 65, 6]

# i = 2
# res 1170
#     next 6
#         res 1164
#             next 65
#                 res 1099
#                     next 3
#                         res 1096 False
#                         res 367 False
#                 res 17.8 False
#             next 365
#                 res 398 False
#                 res 3.2 False
#         res 195
#             next 65
#                 res
#                 res
#     next 656
#         res 514
#         res 1.78
#     next 3656
#         res -2486
#         res 0.3


def is_correct(numbers: list[int], result: int) -> bool:
    return is_correct_3(numbers, result, len(numbers) - 1)


def sum_correct(equations: list[Equation]) -> int:
    result = 0
    for eq in equations:
        if is_correct(eq.numbers, eq.result):
            result += eq.result
    return result


def load_data(filename: str) -> list[Equation]:
    text = Path(__file__).parent.joinpath(filename).read_text()
    data = []
    for line in text.splitlines():
        result, rest = line.split(":")
        data.append(Equation(int(result), [int(n) for n in rest.split()]))

    return data


def main() -> None:
    equations = load_data("data.txt")
    print(sum_correct(equations))


if __name__ == "__main__":
    main()
