from unittest import mock
from pathlib import Path
from tempfile import TemporaryDirectory
import shlex
import pytest
import cards
from cards.cli import app
from typer.testing import CliRunner

runner = CliRunner()


# Sometimes the only way to test is check if something was called,
# use the appropriate assertions on mock objects in those cases
# https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_called

def cards_cli(command_string):
    comamnd_list = shlex.split(command_string)
    result = runner.invoke(app, comamnd_list)
    output = result.stdout.rstrip()
    return output

def test_add_with_owner(mock_cardsdb):
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    mock_cardsdb.add_card.assert_called_with(expected)


# It's also possible to inject errors (exceptions) into calls:
def test_delete_invalid(mock_cardsdb):
    mock_cardsdb.delete_card.side_effect = cards.api.InvalidCardId
    out = cards_cli("delete 25")
    assert "Error: Invalid card id 25" in out
