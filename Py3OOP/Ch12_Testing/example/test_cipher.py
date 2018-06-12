'''
An example of test-driven development using the py.test module.
Run tests with:
py.test --cov-report term (or html, or xml) --cov='myprojectname' '/tests/dir'
'''
from vigenere_cipher import VigenereCipher, combine_character, separate_character
import py.test
import pytest


@pytest.fixture
def cipher():
    return VigenereCipher("TRAIN")


def test_encode(cipher):
    encoded = cipher.encode("ENCODEDINPYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_encode_character(cipher):
    encoded = cipher.encode("E")
    assert encoded == "X"


def test_encode_spaces(cipher):
    encoded = cipher.encode("ENCODED IN PYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_encode_lowercase():
    cipher = VigenereCipher("TRain")
    encoded = cipher.encode("encoded in Python")
    assert encoded == "XECWQXUIVCRKHWA"


def test_combine_character():
    assert combine_character("E", "T") == "X"
    assert combine_character("N", "R") == "E"


def test_extend_keyword(cipher):
    extended = cipher.extend_keyword(16)
    assert extended == "TRAINTRAINTRAINT"


def test_separate_character():
    assert separate_character("X", "T") == "E"
    assert separate_character("E", "R") == "N"


def test_decode(cipher):
    decoded = cipher.decode("XECWQXUIVCRKHWA")
    assert decoded == "ENCODEDINPYTHON"
