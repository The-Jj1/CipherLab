"""Educational ROT13 transformation for ASCII letters."""
from .caesar import encrypt as caesar_encrypt


def encrypt(text: str) -> str:
    return caesar_encrypt(text, 13)


def decrypt(text: str) -> str:
    return encrypt(text)
