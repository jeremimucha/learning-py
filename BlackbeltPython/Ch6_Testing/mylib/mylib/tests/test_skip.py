import pytest

try:
    import mylib
except ImportError:
    mylib = None


@pytest.mark.skip("Do not run this.")
def test_false():
    assert False


@pytest.mark.skipif(mylib is None, reason="mylib is not available")
def test_mylib():
    assert mylib.foobar() == 42


def test_skip_at_runtime():
    if True:
        pytest.skip("Finally I don't want to run it.")
