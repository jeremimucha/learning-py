import pytest
import cards
from cards import Card


# It's also possible to generate both the parameters and their IDs dynamically

def text_variants():
    # This could be data read from a file, database, generated, etc...
    _text_variants = {
    #   ID      Param
        "Short": "x",
        "With Spaces": "x y z",
        "End In Spaces": "x    ",
        "Mixed Case": "SuMmArY wItH MiXeD cAsE",
        "Unicode": "¨©",
        "Newlines": "a\nb\nc",
        "Tabs": "a\tb\tc"
    }
    for key, value in _text_variants.items():
        yield pytest.param(value, id=key)

@pytest.mark.parametrize("variant", text_variants())
def test_summary(cards_db, variant):
    i = cards_db.add_card(Card(summary=variant))
    c = cards_db.get_card()
    assert c.summary == variant
