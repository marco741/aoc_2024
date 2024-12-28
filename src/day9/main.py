from dataclasses import dataclass, field
from pathlib import Path


def expand(s: str) -> list[int | None]:
    result = []
    for i, c in enumerate(s):
        for _ in range(int(c)):
            result.append(i // 2 if i % 2 == 0 else None)
    return result


type Slice = tuple[int, int]


@dataclass
class Expanded:
    files: list[Slice] = field(default_factory=list)
    spaces: list[Slice] = field(default_factory=list)


def expand_less(s: str) -> Expanded:
    res = Expanded()
    j = 0
    for i, char in enumerate(s):
        c = int(char)
        if c == 0:
            continue
        if i % 2 == 0:
            res.files.append((j, j + c))
        else:
            res.spaces.append((j, j + c))
        j += c
    return res


def compress(arr: list[int | None]) -> list[int]:
    i, j = 0, len(arr) - 1
    while i < j:
        while i < j and arr[i] is not None:
            i += 1
        while i < j and arr[i] is None:
            arr[i] = arr[j]
            j -= 1
            while i < j and arr[j] is None:
                j -= 1
    assert not any(x is None for x in arr[:j])
    return arr[: j + 1]  # type: ignore[return-value]


def swap_slices(arr: list[int | None], space_slice: Slice, file_slice: Slice) -> None:
    for i, j in zip(
        range(space_slice[0], space_slice[1]), range(file_slice[0], file_slice[1]), strict=False
    ):
        arr[i], arr[j] = arr[j], arr[i]


def remove_space(space_slices: list[Slice], slice_index: int, remove_length: int) -> None:
    space_slice = space_slices[slice_index]
    space_length = space_slice[1] - space_slice[0]
    if remove_length > space_length:
        raise ValueError
    if remove_length == space_length:
        space_slices.pop(slice_index)
    else:
        space_slices[slice_index] = (
            space_slice[0] + remove_length,
            space_slice[1],
        )


def compress_whole(arr: list[int | None], e: Expanded) -> list[int | None]:
    for i in range(len(e.files) - 1, -1, -1):
        file_slice = e.files[i]
        file_length = file_slice[1] - file_slice[0]

        space_index = None
        for j, space_slice in enumerate(e.spaces):
            if space_slice[0] > file_slice[1]:
                break
            space_length = space_slice[1] - space_slice[0]
            if space_length >= file_length:
                space_index = j
                break

        if space_index is None:
            continue

        remove_space(e.spaces, j, file_length)
        swap_slices(arr, space_slice, file_slice)
    return arr


def checksum(s: str) -> int:
    return sum(i * n for i, n in enumerate(compress(expand(s))))


def checksum_whole(s: str) -> int:
    arr = expand(s)
    expanded = expand_less(s)

    compressed = compress_whole(arr, expanded)
    result = 0
    for i, n in enumerate(compressed):
        if n is None:
            continue
        result += i * n
    return result


def load_data(filename: str) -> str:
    return Path(__file__).parent.joinpath(filename).read_text()


def main() -> None:
    text = load_data("data.txt")
    print(checksum_whole(text))


if __name__ == "__main__":
    main()
