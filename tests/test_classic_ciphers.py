import pytest
from encryption import atbash, vigenere, rail_fence


def test_known_examples():
    assert atbash.encrypt("Hello World!") == "Svool Dliow!"
    assert vigenere.encrypt("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"
    assert vigenere.decrypt("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"
    assert rail_fence.encrypt("WEAREDISCOVEREDFLEEATONCE", 3) == "WECRLTEERDSOEEFEAOCAIVDEN"
    assert rail_fence.decrypt("WECRLTEERDSOEEFEAOCAIVDEN", 3) == "WEAREDISCOVEREDFLEEATONCE"


@pytest.mark.parametrize("text", ["", "A", "Hello World!", "Здравей 🌍\nTabs\t  ", "AaZz0123!?"])
def test_round_trips(text):
    assert atbash.decrypt(atbash.encrypt(text)) == text
    for key in ("a", "LEMON", "MixedCase"):
        assert vigenere.decrypt(vigenere.encrypt(text, key), key) == text
    for rails in (2, 3, 4, 100):
        assert rail_fence.decrypt(rail_fence.encrypt(text, rails), rails) == text


def test_vigenere_ignores_non_ascii_for_key_position():
    assert vigenere.encrypt("A Б!A", "BC") == "B Б!C"


@pytest.mark.parametrize("key", ["", "123", "secret key", "ключ", "A!"])
def test_invalid_keyword(key):
    for action in (vigenere.encrypt, vigenere.decrypt):
        with pytest.raises(ValueError):
            action("hello", key)


@pytest.mark.parametrize("rails", [-3, 0, 1, 101, 3.5, True])
def test_invalid_rails(rails):
    for action in (rail_fence.encrypt, rail_fence.decrypt):
        with pytest.raises(ValueError):
            action("hello", rails)
