import pytest
import time


# Sometimes we might want to run some code (fixture)
# for every test case, without the need to explicitly
# including that fixture in the parameter list,
# this can be achieved with `autouse`

# run with `-v -s` to see the info printed by fixtures:
# `pytest -v -s test_autouse.py`
# `-s` is short for `--capture=no`


@pytest.fixture(autouse=True, scope="session")
def footer_session_scope():
    """Report the time at the end of a session."""
    yield
    now = time.time()
    print("--")
    print(
        "finished: {}".format(
            time.strftime("%d %b %X", time.localtime(now))
        )
    )

@pytest.fixture(autouse=True)
def footer_function_scope():
    """Report test durations after each function"""
    start = time.time()
    yield
    stop = time.time()
    delta = stop - start
    print("\ntest duration : {:0.3} seconds".format(delta))

def test_1():
    "Simulate long-ish running test."
    time.sleep(1)

def test_2():
    """Simulate slightly longer test."""
    time.sleep(1.23)
