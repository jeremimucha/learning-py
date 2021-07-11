import pytest


# test this, if executed with -m dicttest
# skip if excuted with -m 'not dicttest'
@pytest.mark.dicttest
def test_something():
    a = ['a', 'b']
    b = ['b']


def test_something_else():
    assert False
