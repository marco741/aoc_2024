import itertools
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import numpy as np
from tqdm import tqdm

type Coord = tuple[int, int]
type Matrix = list[list[int | None]]


@dataclass
class Machine:
    a: Coord
    b: Coord
    prize: Coord


A_COST = 3
B_COST = 1


def load_data(filename: str) -> list[Machine]:
    result = []
    data = Path(__file__).parent.joinpath(filename).read_text()

    machine_chunks = data.split("\n\n")
    for mc in machine_chunks:
        lines = mc.splitlines()
        assert len(lines) == 3
        a, b, prize = tuple(line.split(": ")[1] for line in lines)

        buttons: list[Coord] = []
        button_chunks: tuple[str, str] = a, b
        for bc in button_chunks:
            button = tuple(int(c.split("+")[1]) for c in bc.split(", "))
            assert len(button) == 2
            buttons.append(button)

        prize_coord = tuple(int(c.split("=")[1]) for c in prize.split(", "))
        assert len(prize_coord) == 2
        result.append(Machine(buttons[0], buttons[1], prize_coord))

    return result


def minimum_tokens(machine: Machine, a_cost: int, b_cost: int) -> int | None:
    @cache
    def memo(tokens: int, x: int, y: int) -> int | None:
        if (x, y) == machine.prize:
            return tokens
        if x > machine.prize[0] or y > machine.prize[1]:
            return None

        new_tokens: list[int] = []
        for (x0, y0), cost in ((machine.a, a_cost), (machine.b, b_cost)):
            new_token = memo(tokens + cost, x + x0, y + y0)
            if new_token is not None:
                new_tokens.append(new_token)
        return min(new_tokens, default=None)

    return memo(0, 0, 0)


def read(matrix: Matrix, x: int, y: int) -> int | None:
    if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
        return matrix[x][y]
    return None


def minimum_tokens_dp(machine: Machine, a_cost: int, b_cost: int) -> int | None:
    n, m = machine.prize
    dp: Matrix = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for x, y in itertools.product(range(n + 1), range(m + 1)):
        for (x0, y0), cost in ((machine.a, a_cost), (machine.b, b_cost)):
            old_value = read(dp, x - x0, y - y0)
            if old_value is None:
                continue
            old_value += cost
            cur_value = read(dp, x, y)
            dp[x][y] = min(
                (v for v in (old_value, cur_value) if v is not None), default=None
            )
    return dp[-1][-1]


def minimum_tokens_dp_dict(machine: Machine, a_cost: int, b_cost: int) -> int | None:
    n, m = machine.prize
    dp: defaultdict[Coord, int] = defaultdict(lambda: sys.maxsize)
    dp[(0, 0)] = 0

    while len(dp):
        new_dp: defaultdict[Coord, int] = defaultdict(lambda: sys.maxsize)
        for (x, y), tokens in dp.items():
            for (x0, y0), cost in ((machine.a, a_cost), (machine.b, b_cost)):
                if (x + x0) > n or (y + y0) > m:
                    continue
                old_tokens = new_dp[(x + x0, y + y0)]
                if x + x0 == n and y + y0 == m and old_tokens != sys.maxsize:
                    return min(old_tokens, tokens + cost)
                new_dp[(x + x0), (y + y0)] = min(old_tokens, tokens + cost)
        dp = new_dp
    return None


def mcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def mcm(a: int, b: int) -> int:
    return a * b // mcd(a, b)


def minimum_tokens_dp_dict_modulo(
    machine: Machine, a_cost: int, b_cost: int
) -> int | None:
    n = min(machine.prize[0], mcm(machine.a[0], machine.b[0])) + 1
    m = min(machine.prize[1], mcm(machine.a[1], machine.b[1])) + 1
    n, m = min(mcm(n, m), machine.prize[0]), min(mcm(n, m), machine.prize[1])
    dp: defaultdict[Coord, int] = defaultdict(lambda: sys.maxsize)
    dp[(0, 0)] = 0

    result = sys.maxsize
    while len(dp):
        new_dp: defaultdict[Coord, int] = defaultdict(lambda: sys.maxsize)
        for (x, y), tokens in dp.items():
            for (x0, y0), cost in ((machine.a, a_cost), (machine.b, b_cost)):
                x1, y1 = x + x0, y + y0
                if x1 > n or y1 > m:
                    continue
                old_tokens = new_dp[x1, y1]

                new_dp[x1, y1] = min(old_tokens, tokens + cost)

                if (
                    machine.prize[0] % x1 == 0
                    and machine.prize[1] % y1 == 0
                    and machine.prize[0] // x1 == machine.prize[1] // y1
                ):
                    result = min(result, (tokens + cost) * machine.prize[0] // x1)

        dp = new_dp
    return result if result != sys.maxsize else None


def get_sorted_buttons(
    a: Coord, b: Coord
) -> tuple[tuple[Coord, int], tuple[Coord, int]]:
    a_cost, b_cost = A_COST, B_COST
    if a[0] - (b[0] * 3) + a[1] - (b[1] * 3) < 0:
        a, b = b, a
        a_cost, b_cost = b_cost, a_cost
    return (a, a_cost), (b, b_cost)


def minimum_tokens_greedy(machine: Machine) -> int | None:
    p0, p1 = machine.prize
    (a, a_cost), (b, b_cost) = (machine.a, A_COST), (machine.b, B_COST)
    result = sys.maxsize
    for _ in range(2):
        tokens = 0
        a, b = b, a
        a_cost, b_cost = b_cost, a_cost
        while p0 >= 0 and p1 >= 0:
            if p0 % b[0] == 0 and p1 % b[1] == 0:
                result = min(result, tokens + p0 // b[0] * b_cost)
                break
            p0 -= a[0]
            p1 -= a[1]
            tokens += a_cost
    return result if result != sys.maxsize else None


def minimum_tokens_math(machine: Machine, a_cost: int, b_cost: int) -> int | None:
    p0, p1 = machine.prize
    a0, a1 = machine.a
    b0, b1 = machine.b
    try:
        a_tokens = (p0 / a0) - (b0 * (a1 * p0 - a0 * p1)) / (a0 * (b0 * a1 - b1 * a0))
        b_tokens = (a1 * p0 - a0 * p1) / (b0 * a1 - b1 * a0)
    except ZeroDivisionError:
        return None
    if (
        not math.isclose(a_tokens, round(a_tokens), rel_tol=0, abs_tol=1e-3)
        or not math.isclose(b_tokens, round(b_tokens), rel_tol=0, abs_tol=1e-3)
        or a_tokens < 0
        or b_tokens < 0
    ):
        return None
    return round(a_tokens) * a_cost + round(b_tokens) * b_cost


def minimum_tokens_np(machine: Machine, a_cost: int, b_cost: int) -> int | None:
    try:
        result = np.linalg.solve(np.transpose([machine.a, machine.b]), machine.prize)
        press_a = float(result[0])
        press_b = float(result[1])
    except np.linalg.LinAlgError:
        return None
    if (
        not math.isclose(press_a, round(press_a), rel_tol=0, abs_tol=1e-3)
        or not math.isclose(press_b, round(press_b), rel_tol=0, abs_tol=1e-3)
        or press_a < 0
        or press_b < 0
    ):
        return None
    return round(press_a) * a_cost + round(press_b) * b_cost


def increase_prizes(machines: list[Machine], amount: int) -> None:
    for m in machines:
        m.prize = m.prize[0] + amount, m.prize[1] + amount


def main() -> None:
    machines = load_data("data.txt")
    increase_prizes(machines, 10000000000000)
    print(sum(minimum_tokens_np(m, A_COST, B_COST) or 0 for m in tqdm(machines)))


if __name__ == "__main__":
    main()
