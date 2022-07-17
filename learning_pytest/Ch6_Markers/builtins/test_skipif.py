import pytest
from packaging.version import parse
import cards


@pytest.mark.skipif(
    parse(cards.__version__).major < 2,
    reason="Card < comparison not supported in 1.x",
)
def test_less_than():
    c1 = cards.Card("a task")
    c2 = cards.Card("a task")
    assert c1 < c2
