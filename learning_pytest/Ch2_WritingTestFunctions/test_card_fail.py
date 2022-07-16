from cards import Card


def test_equality():
    c1 = Card("sit there", "brian")
    c2 = Card("do something", "okken")
    assert c1 == c2
