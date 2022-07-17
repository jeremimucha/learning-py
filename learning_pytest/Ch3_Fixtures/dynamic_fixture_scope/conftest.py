from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
import cards


# Sometimes it might be necessary to decide the scope of a fixture
# at runtime, rather than hardcoding it statically.
# To achieve this, we can define a function, or other callable,
# that returns the fixture scope, having analyzed the given
# config context.

# Call this test package with and without `--func-db` to see it in action.


def db_scope(fixture_name, config):
    if config.getoption("--func-db", None):
        return "function"
    return "session"

# Config hook, which adds a `--func-db` flag
def pytest_addoption(parser):
    parser.addoption(
        "--func-db",
        action="store_true",
        default=False,
        help="new db for each test",
    )


@pytest.fixture(scope=db_scope)
def cards_db_session():
    """CardsDb object connected to a temporary database"""
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        db.close()

@pytest.fixture(scope='function')
def cards_db(cards_db_session):
    """CardsDB object that's empty"""
    cards_db_session.delete_all()
    return cards_db_session


@pytest.fixture(scope="session")
def some_cards():
    """List of different Card objects"""
    return [
        cards.Card("write book", "Brian", "done"),
        cards.Card("edit book", "Katie", "done"),
        cards.Card("write 2nd edition", "Brian", "todo"),
        cards.Card("edit 2nd edition", "Katie", "todo"),
    ]

# Fixtures may also use multiple other fixtures:
@pytest.fixture(scope="function")
def non_empty_db(cards_db, some_cards):
    """CardsDB object that's been populated with 'some_cards"""
    for c in some_cards:
        cards_db.add_card(c)
    return cards_db
