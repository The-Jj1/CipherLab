import pytest
from encryption import caesar, rot13


def test_known_example():
    assert caesar.encrypt("Hello World!", 3) == "Khoor Zruog!"
    assert caesar.decrypt("Khoor Zruog!", 3) == "Hello World!"


@pytest.mark.parametrize("shift", [-105, -26, -1, 0, 3, 26, 105])
@pytest.mark.parametrize("text", ["", "Az Za! 123", "Здравей 🌍\nHello\t "])
def test_round_trip(text, shift):
    assert caesar.decrypt(caesar.encrypt(text, shift), shift) == text


def test_unicode_untouched():
    assert caesar.encrypt("Здравей 🌍", 3) == "Здравей 🌍"


def test_rot13():
    assert rot13.encrypt("Hello World!") == "Uryyb Jbeyq!"
    assert rot13.decrypt(rot13.encrypt("Здравей, World!")) == "Здравей, World!"
