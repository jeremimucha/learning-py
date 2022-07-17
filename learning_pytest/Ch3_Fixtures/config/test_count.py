import pytest
import cards


# Uses fixture from conftest.py
# Note that conftest is not imported here,
# this is handled automatically by pytest.

# Use `--fixtures -v` to show where the used fixtures are defined
# Or use `--fixtures-per-test` to see which fixture each test
# uses and where they're defined.


def test_empty(cards_db):
    assert cards_db.count() == 0


def test_two(cards_db):
    cards_db.add_card(cards.Card("first"))
    cards_db.add_card(cards.Card("second"))
    assert cards_db.count() == 2

