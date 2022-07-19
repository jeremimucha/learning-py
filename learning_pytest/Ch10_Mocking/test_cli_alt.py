from unittest import mock
from pathlib import Path
from tempfile import TemporaryDirectory
import shlex
import pytest
import cards
from cards.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def cards_cli(command_string):
    comamnd_list = shlex.split(command_string)
    result = runner.invoke(app, comamnd_list)
    output = result.stdout.rstrip()
    return output

# An alternative approach to testing the cli interface,
# without using mocks.
# Here we rely on the side effects of the behavior we're testing.
def test_add_with_owner(cards_db):
    """
    A cardshows up in the list with expected contents.
    """
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    all_cards = cards_db.list_cards()
    assert len(all_cards) == 1
    assert all_cards[0] == expected
