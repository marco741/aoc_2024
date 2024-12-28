import re
from pathlib import Path


def multiply_if_enabled(text: str) -> int:
    mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)", re.RegexFlag.MULTILINE)
    enable_pattern = re.compile(r"(do\(\)|don't\(\))", re.RegexFlag.MULTILINE)
    sections = [0]
    enabled = True
    for match in enable_pattern.finditer(text):
        if len(match.group()) == 7 and enabled:
            enabled = False
            sections.append(match.start())
        elif len(match.group()) == 4 and not enabled:
            sections.append(match.start())
            enabled = True
    print(sections)

    result = 0
    i = 0
    for match in mul_pattern.finditer(text):
        while i + 1 < len(sections) and sections[i + 1] < match.start():
            i += 1
        if i % 2 == 0:
            v1, v2 = match.groups()
            result += int(v1) * int(v2)
    return result


def parse_and_multiply(text: str) -> int:
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)", re.RegexFlag.MULTILINE)
    result = 0
    for match in pattern.finditer(text):
        v1, v2 = match.groups()
        result += int(v1) * int(v2)
    return result


def load_data(filename: str) -> str:
    filepath = Path(__file__).parent.joinpath(filename)

    return filepath.read_text()


def main() -> None:
    filename = "data.txt"
    text = load_data(filename)
    print(multiply_if_enabled(text))


if __name__ == "__main__":
    main()
