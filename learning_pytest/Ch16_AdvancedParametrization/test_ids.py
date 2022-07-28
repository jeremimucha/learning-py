import pytest
import cards
from cards import Card


@pytest.mark.parametrize("start_state", ["done", "in prog", "todo"])
def test_finish(cards_db, start_state):
    c = Card("write a book", state=start_state)
    index = cards_db.add_card(c)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"


# Using objects, rather than plain strings for parametrization
# results in pytest not being able to print the parameters nicely.
# Instead, pytest will just enumarate the parameters:
# `starting_card0`, `starting_card1`, ...
# To get around this issue and improve readability, we can define
# custom identifiers
@pytest.mark.parametrize(
    "starting_card",
    [
        Card("foo", state="todo"),
        Card("foo", state="in prog"),
        Card("foo", state="done"),
    ],
)
def test_card(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"

_card_list = [
    Card("foo", state="todo"),
    Card("foo", state="in prog"),
    Card("foo", state="done"),
],


# --------------------------------------------------------------------------------------------------------------------
# We can use simple str() conversion to provide the parameter ID:
# --------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "starting_card",
    *_card_list,
    # just use str() conversion for the id method
    # This works, but hides the important details in a lot of other noise.
    ids=str
)
def test_id_str(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"
# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
# We can implement and pass in our own custom id functions.
# This is an improvement, since we can narrow down the output
# to jsut the relevant parts.
# --------------------------------------------------------------------------------------------------------------------
def card_state(card: Card):
    return card.state

@pytest.mark.parametrize("starting_card", *_card_list, ids=card_state)
def test_id_func(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"
# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
# It's also possible to specify custom `id` function to `pytest.param`s
# --------------------------------------------------------------------------------------------------------------------
_c_list = [
    Card("foo", state="todo"),
    pytest.param(Card("foo", state="in prog"), id="special"),
    Card("foo", state="done"),
]

@pytest.mark.parametrize("starting_card", _c_list, ids=card_state)
def test_id_param(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"
# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
# Another simple way to specify param ids, is to just pass in an explicit list of ids.
# The downside here is that the list of params and ids need to be synchronized manually.
# --------------------------------------------------------------------------------------------------------------------
_id_list = ["todo", "in prog", "done"]
@pytest.mark.parametrize("starting_card", _c_list, ids=_id_list)
def test_id_list(cards_db, starting_card):
    index = cards_db.add_card(starting_card)
    cards_db.finish(index)
    card = cards_db.get_card(index)
    assert card.state == "done"

# One way to achieve the synchronization of parameters and ids is to use a dict() and pass in .keys() and .values()
# as params and ids. This takes the advantage of a guarantee that .keys() and .values() views into the dictionary
# are lined up.
text_variants = {
#   ID      Param
    "Short": "x",
    "With Spaces": "x y z",
    "End In Spaces": "x    ",
    "Mixed Case": "SuMmArY wItH MiXeD cAsE",
    "Unicode": "¨©",
    "Newlines": "a\nb\nc",
    "Tabs": "a\tb\tc"
}
@pytest.mark.parametrize("variant", text_variants.values(), ids=text_variants.keys())
def test_summary_variants(cards_db, variant):
    i = cards_db.add_card(Card(summary=variant))
    c = cards_db.get_card(i)
    assert c.summary == variant
# --------------------------------------------------------------------------------------------------------------------