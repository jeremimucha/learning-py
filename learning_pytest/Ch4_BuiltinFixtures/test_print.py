import pytest

# Normally, pytest captures and silences thee stdout/stderr unless a test fails.
# This can be changed by passing `-s/--capture=no` flag on the commandline.
# A more finegrained way to control this behavior is to to use `capsys.disabled()`

def test_normal():
    # no output unless with `-s/--capture=no`
    print("\nnormal print")

def test_fail():
    # output always shown for failing tests
    print("\nprint in failing test")
    assert False

def test_disabled(capsys):
    # This output will always be displayed,
    # even without `-s/--capture=no`
    with capsys.disabled():
        print("\ncapsys disabled print")
