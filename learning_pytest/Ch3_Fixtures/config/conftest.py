from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
import cards


# Fixture initialized once per session.
# We might want to do this, to avoid the cost of initializing
# the fixture for every function.
# However this may lead to issues, due to persistent state of
# the fixture.
# To avoid this issue we can introduce a second fixture,
# that relies on this one, but performs some cleanup
# action, that's cheaper then full re-initialization,
# but still ensures that each test-case is independent.
@pytest.fixture(scope="session")
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


# Convenience fixture we might want to reuse, to avoid re-initializing common
# Card objects throughout test cases.
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
