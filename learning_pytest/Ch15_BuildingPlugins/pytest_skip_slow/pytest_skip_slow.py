"""
A pytest plugin to skip `@pytest.mark.slow` tests by default.
Imclude the slow tests with `--slow`.
"""
import pytest
__version__ = "0.1.0"


def pytest_configure(config):
    """
    Adds a `slow` marker to the pytest.ini file, so that it doesn't need to
    be done explicitly everytime.
    """
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_addoption(parser):
    parser.addoption(
        "--slow", action="store_true", help="include tests marked slow"
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--slow"):
        skip_slow = pytest.mark.skip(reason="need --slow option to run")
        for item in items:
            if item.get_closest_marker("slow"):
                item.add_marker(skip_slow)
