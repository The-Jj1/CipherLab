"""Authenticated text encryption using cryptography's Fernet implementation."""
from cryptography.fernet import Fernet, InvalidToken


def generate_key() -> str:
    return Fernet.generate_key().decode("ascii")


def validate_key(key: str) -> None:
    try:
        Fernet(key.encode("ascii"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Enter a valid Fernet key or generate a new one.") from exc


def encrypt(text: str, key: str) -> str:
    validate_key(key)
    return Fernet(key.encode("ascii")).encrypt(text.encode("utf-8")).decode("ascii")


def decrypt(text: str, key: str) -> str:
    validate_key(key)
    try:
        return Fernet(key.encode("ascii")).decrypt(text.strip().encode("ascii")).decode("utf-8")
    except (InvalidToken, UnicodeError) as exc:
        raise ValueError("Decryption failed: wrong key, damaged token, or non-text content.") from exc
