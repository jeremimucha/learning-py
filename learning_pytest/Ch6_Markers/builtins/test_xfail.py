import pytest
from packaging.version import parse
import cards


# Will fail, as expected
@pytest.mark.xfail(
    parse(cards.__version__).major < 2,
    reason="Card < comparison not supported in 1.x"
)
def test_less_than():
    c1 = cards.Card("a task")
    c2 = cards.Card("b task")
    assert c1 < c2


# Marked for failure, but will actually pass.
# Since the xfail isn't strict, passing this test
# will result in only a warning
@pytest.mark.xfail(reason="XPASS demo")
def test_xpass():
    c1 = cards.Card("a task")
    c2 = cards.Card("a task")
    assert c1 == c2

# Strict xfail - if this test passes the test case fails.
@pytest.mark.xfail(reason="strict demo", strict=True)
def test_xfail_strict():
    c1 = cards.Card("a task")
    c2 = cards.Card("a task")
    assert c1 == c2
