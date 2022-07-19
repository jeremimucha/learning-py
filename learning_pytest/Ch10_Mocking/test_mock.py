from unittest import mock

import pytest
import cards
from cards.cli import app
from typer.testing import CliRunner

runner = CliRunner()


# @pytest.fixture()
# def mock_cardsdb():
#     # autospec=True here ensures that the mock accepts only calls that
#     # match the interface of the mocked object.
#     # Without it, python mocks are too permissive - they accept virtually any call.
#     with mock.patch.object(cards, "CardsDB", autospec=True) as MockCardsDB:
#         yield MockCardsDB.return_value


def test_mock_version():
    with mock.patch.object(cards, '__version__', "1.2.3"):
        result = runner.invoke(app, ["version"])
        assert result.stdout.rstrip() == "1.2.3"


# Mocking the cards/cli.py config()
def test_mock_CardsDB():
    with mock.patch.object(cards, "CardsDB") as MockCardsDB:
        print()
        print(f"       class:{MockCardsDB}")
        print(f"return_value:{MockCardsDB.return_value}")
        with cards.cli.cards_db() as db:
            print(f"    object:{db}")

def test_mock_path():
    with mock.patch.object(cards, "CardsDB") as MockCardsDB:
        MockCardsDB.return_value.path.return_value = "/foo/"
        with cards.cli.cards_db() as db:
            print()
            print(f"{db.path=}")
            print(f"{db.path()=}")

# Using the mock_cardsdb():
def test_config(mock_cardsdb):
    mock_cardsdb.path.return_value = "/foo/"
    result = runner.invoke(app, ["config"])
    assert result.stdout.rstrip() == "/foo/"


# Demonstrate issues with non-autospec mocks
def test_bad_mock():
    with mock.patch.object(cards, "CardsDB") as CardsDB:
        db = CardsDB("/some/path")
        db.path()       # good
        db.path(35)     # Invalid arguments, but a non-autospec mock accepts this anyway
        db.not_valid()  # Invalid function, but non-autospec mock still accepts this
