"""Educational Caesar cipher. Only ASCII letters are shifted."""


def encrypt(text: str, shift: int = 3) -> str:
    result = []
    for char in text:
        if "A" <= char <= "Z":
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif "a" <= char <= "z":
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return "".join(result)


def decrypt(text: str, shift: int = 3) -> str:
    return encrypt(text, -shift)
