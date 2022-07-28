import pytest
import cards
from cards import Card


# Tests can be parameterized with multiple parameters.
# In simple cases we can specify the parameter values as a list of tuples.
@pytest.mark.parametrize(
    "summary, owner, state",
    [
        ("short", "First", "todo"),
        ("short", "First", "in prog"),
        # ...
    ]
)
def test_add_lots(cards_db, summary, owner, state):
    """
    Make sure adding to db doesn't change values.
    """
    i = cards_db.add_card(Card(summary, owner=owner, state=state))
    card = cards_db.get_card(i)

    expected = Card(summary, owner=owner, state=state)
    assert card == expected


# In more complex cases, when we have lots of combinations that we need to test
# it's better to parameter-stack:
_states = ["todo", "in prog", "done"]
_owners = ["First"]
_summaries = ["short"]
@pytest.mark.parametrize("state", _states)
@pytest.mark.parametrize("owner", _owners)
@pytest.mark.parametrize("summary", _summaries)
def test_stacking(cards_db, summary, owner, state):
    """
    Make sure adding to db doesn't change values.
    """
    i = cards_db.add_card(Card(summary, owner=owner, state=state))
    card = cards_db.get_card(i)
    expected = Card(summary, owner=owner, state=state)
    assert card == expected
