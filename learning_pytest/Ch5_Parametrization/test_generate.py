import pytest
from cards import Card


# Builtin pytest hook function.
# This is a very simple example, but the `pytest_generate_test` hook
# is very powerful thanks to access to the metafunc:
# https://docs.pytest.org/en/latest/reference/reference.html#metafunc
def pytest_generate_test(metafunc):
    if "start_state" in metafunc.fixturenames:
        metafunc.parametrize("start_state", ["done", "in prog", "todo"])


def test_finish(cards_db, start_state):
    c = Card("write a book", state=start_state)
    index = cards_db.add_card(c)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"
