"""Educational Vigenere cipher. Only ASCII letters consume key positions."""

def _transform(text: str, key: str, direction: int) -> str:
    if not key or any(not ("a" <= char <= "z" or "A" <= char <= "Z") for char in key):
        raise ValueError("Keyword must contain only English letters A–Z.")
    shifts = [ord(char.lower()) - 97 for char in key]
    result = []
    position = 0
    for char in text:
        if "A" <= char <= "Z" or "a" <= char <= "z":
            base = 65 if char <= "Z" else 97
            shift = shifts[position % len(shifts)] * direction
            result.append(chr((ord(char) - base + shift) % 26 + base))
            position += 1
        else:
            result.append(char)
    return "".join(result)


def encrypt(text: str, key: str) -> str:
    return _transform(text, key, 1)


def decrypt(text: str, key: str) -> str:
    return _transform(text, key, -1)
