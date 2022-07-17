import pytest
import cards


# Markers can also be parameterized, just like the builtin markers.
# Not only that, markers can be parameterized.


# If we didn't parameterize the markers/fixtures
@pytest.fixture(scope="function")
def cards_db_three_cards(cards_db_session):
    db = cards_db_session
    # start with empty
    db.delete_all()
    # add three cards
    db.add_card(cards.Card("Learn something new"))
    db.add_card(cards.Card("Build useful tools"))
    db.add_card(cards.Card("Teach others"))
    return db


def test_zero_card(cards_db):
    assert cards_db.count() == 0

def test_three_card(cards_db_three_cards):
    cards_db = cards_db_three_cards
    assert cards_db.count() == 3


