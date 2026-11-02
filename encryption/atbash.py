"""Educational ASCII alphabet reflection. Not secure encryption."""

def encrypt(text: str) -> str:
    result = []
    for char in text:
        if "A" <= char <= "Z":
            result.append(chr(90 - (ord(char) - 65)))
        elif "a" <= char <= "z":
            result.append(chr(122 - (ord(char) - 97)))
        else:
            result.append(char)
    return "".join(result)


def decrypt(text: str) -> str:
    return encrypt(text)
