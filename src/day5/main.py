from collections import defaultdict, deque
from pathlib import Path


def get_ok_links(graph: dict[int, set[int]], ok: set[int], cur: int, seen: set[int]) -> set[int]:
    ok_links: set[int] = set()
    q: deque[int] = deque()
    for node in graph.get(cur, set()):
        q.append(node)
    while len(q):
        cur = q.popleft()
        if cur in seen:
            continue
        if cur in ok:
            ok_links.add(cur)
        else:
            for node in graph.get(cur, set()):
                q.append(node)

    return ok_links


def is_sorted(graph: dict[int, set[int]], update: list[int]) -> bool:
    ok: set[int] = set(update)
    seen: set[int] = set()
    for n in update:
        if n in seen:
            return False
        for forbidden in graph.get(n, set()) & ok:
            seen.add(forbidden)
    return True


def sort(graph: dict[int, set[int]], update: list[int]) -> list[int]:
    ok: set[int] = set(update)
    i = 0
    while i < len(update) - 1:
        wrong = graph.get(update[i], set()) & ok
        if not len(wrong):
            ok.remove(update[i])
            i += 1
            continue
        node = wrong.pop()
        j = update.index(node)
        update[i], update[j] = update[j], update[i]
    return update


def sum_of_middles(graph: dict[int, set[int]], updates: list[list[int]]) -> int:
    result = 0
    for update in updates:
        if is_sorted(graph, update):
            result += update[len(update) // 2]
    return result


def sum_of_unsorted(graph: dict[int, set[int]], updates: list[list[int]]) -> int:
    result = 0
    for update in updates:
        if not is_sorted(graph, update):
            update = sort(graph, update)
            result += update[len(update) // 2]
    return result


def load_data(filename: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    filepath = Path(__file__).parent.joinpath(filename)

    graph: dict[int, set[int]] = defaultdict(set)
    text = filepath.read_text()
    graph_text, updates = text.split("\n\n")
    for line in graph_text.splitlines():
        node, link = line.split("|")
        graph[int(link)].add(int(node))

    updates_list = [list(map(int, u.split(","))) for u in updates.splitlines()]

    return graph, updates_list


def main() -> None:
    graph, updates_list = load_data("data.txt")
    print(sum_of_unsorted(graph, updates_list))


if __name__ == "__main__":
    main()
