from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
import cards


# Sometimes initializing a test fixture might be expensive,
# and we might not want to re-initialize it for every single
# new test-case, to avoid the initialization cost.
# This can be achieved by changing the fixture scope,
# so that the fixture is initialized e.g. once per
# module, or class, etc.
#
# Available scopes:
# - function [default] - run once per test function
# - class
# - module
# - package (test directory)
# - session
#
# The `package` and `session` scopes can only be used
# if a fixture is defined in `conftest.py`


# Fixture initialized once per module:
@pytest.fixture(scope="module")
def cards_db():
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        db.close()


def test_empty(cards_db):
    assert cards_db.count() == 0

def test_Two(cards_db):
    cards_db.add_card(cards.Card("first"))
    cards_db.add_card(cards.Card("second"))
    assert cards_db.count() == 2
