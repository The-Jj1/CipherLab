"""Educational zigzag transposition, preserving every Unicode code point."""

def _validate(rails: int) -> None:
    if isinstance(rails, bool) or not isinstance(rails, int) or not 2 <= rails <= 100:
        raise ValueError("Rail count must be a whole number between 2 and 100.")


def _path(length: int, rails: int):
    period = 2 * (rails - 1)
    for index in range(length):
        step = index % period
        yield min(step, period - step)


def encrypt(text: str, rails: int = 3) -> str:
    _validate(rails)
    rows = [[] for _ in range(min(rails, len(text))) ]
    for char, row in zip(text, _path(len(text), rails)):
        rows[row].append(char)
    return "".join("".join(row) for row in rows)


def decrypt(text: str, rails: int = 3) -> str:
    _validate(rails)
    path = list(_path(len(text), rails))
    counts = [0] * rails
    for row in path:
        counts[row] += 1
    rows = []
    offset = 0
    for count in counts:
        rows.append(iter(text[offset:offset + count]))
        offset += count
    return "".join(next(rows[row]) for row in path)
