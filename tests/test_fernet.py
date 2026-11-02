import pytest
from encryption import fernet_cipher as cipher


@pytest.mark.parametrize("text", ["", "Hello World!", "Здравей 🌍\n\t trailing  "])
def test_round_trip(text):
    key = cipher.generate_key()
    assert cipher.decrypt(cipher.encrypt(text, key), key) == text


def test_randomized_tokens():
    key = cipher.generate_key()
    assert cipher.encrypt("same", key) != cipher.encrypt("same", key)


def test_wrong_key():
    token = cipher.encrypt("secret", cipher.generate_key())
    with pytest.raises(ValueError, match="Decryption failed"):
        cipher.decrypt(token, cipher.generate_key())


def test_tampering():
    key = cipher.generate_key()
    token = cipher.encrypt("secret", key)
    pos = len(token) // 2
    changed = token[:pos] + ("A" if token[pos] != "A" else "B") + token[pos + 1:]
    with pytest.raises(ValueError):
        cipher.decrypt(changed, key)


@pytest.mark.parametrize("key", ["", "not-a-key", "ключ"])
def test_invalid_key(key):
    with pytest.raises(ValueError, match="valid Fernet key"):
        cipher.encrypt("text", key)


@pytest.mark.parametrize("token", ["", "not a token", "невалидно"])
def test_bad_token(token):
    with pytest.raises(ValueError, match="Decryption failed"):
        cipher.decrypt(token, cipher.generate_key())
