from cards import Card


# We can run this test file and specify that we'd like to run
# only a specific test class grouping a set of test cases
# `pytest -v test_classes.py::TestEquality`
# or even a single method
# `pytest -v test_classes.py::TestEquality::test_equality`

class TestEquality:
    def test_equality(self):
        c1 = Card("something", "brian", "todo", 123)
        c2 = Card("something", "brian", "todo", 123)
        assert c1 == c2

    def test_equality_with_diff_ids(self):
        c1 = Card("something", "brian", "todo", 123)
        c2 = Card("different", "okken", "done", 123)
        assert c1 != c2

    def test_inequality(self):
        c1 = Card("something", "brian", "todo", 123)
        c2 = Card("completely different", "okken", "done", 123)
        assert c1 != c2
