from unittest import mock
from pathlib import Path
from tempfile import TemporaryDirectory
import shlex
import pytest
import cards


@pytest.fixture(scope="session")
def cards_db_session(tmp_path_factory):
    """CardsDb object connected to a temporary database"""
    db_path = tmp_path_factory.mktemp("cards_db")
    db = cards.CardsDB(db_path)
    yield db
    db.close()



@pytest.fixture(scope='function')
def cards_db(cards_db_session, request, faker):
    """CardsDB object that's empty"""
    db = cards_db_session
    db.delete_all()

    # support for `@pytest.mark.num_cards(<some-number>)`
    # random seed
    # https://faker.readthedocs.io
    faker.seed_instance(101)
    m = request.node.get_closest_marker("num_cards")
    if m and len(m.args) > 0:
        num_cards = m.args[0]
        for _ in range(num_cards):
            db.add_card(
                cards.Card(summary=faker.sentence(), owner=faker.first_name())
            )
    return db


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


@pytest.fixture()
def mock_cardsdb():
    # autospec=True here ensures that the mock accepts only calls that
    # match the interface of the mocked object.
    # Without it, python mocks are too permissive - they accept virtually any call.
    # https://docs.python.org/3/library/unittest.mock.html#autospeccing
    with mock.patch.object(cards, "CardsDB", autospec=True) as MockCardsDB:
        yield MockCardsDB.return_value
