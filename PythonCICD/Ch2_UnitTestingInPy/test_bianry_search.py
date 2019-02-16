from binary_search import search


def test_search_middle():
    assert search(2, [1, 2, 3, 4]) == 1, 'expected to find 2 at index 1'

def test_search_first():
    assert search(1, [1, 2, 3, 4]) == 0, 'expected to find 1 at index 0'

def test_search_last():
    assert search(4, [1, 2, 3, 4]) == 3, 'expected to find 4 at index 3'


def test_exception_not_found():
    from pytest import raises

    with raises(ValueError):
        search(-1, [1, 2, 3, 4])

    with raises(ValueError):
        search(5, [1, 2, 3, 4])

    with raises(ValueError):
        search(2, [1, 3, 4])
