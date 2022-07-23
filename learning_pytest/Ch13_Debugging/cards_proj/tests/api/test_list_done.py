"""
Test cases
* list cards in 'done' state
"""
import pytest


@pytest.mark.num_cards(10)
def test_list_done(cards_db):
    cards_db.finish(3)
    cards_db.finish(5)

    done_cards = cards_db.list_done_cards()

    assert len(done_cards) == 2
    for card in done_cards:
        assert card.id in (3, 5)
        assert card.state == "done"
