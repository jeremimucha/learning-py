'''
The py.test module offers a completely different way to setup and teardown
class and module variables - funcargs.
Funcargs are basically named variables taht are  predefined in a test
configuration file. This allows us to separate configuration from execution
of tests and allows funcargs to be used across multiple classes and modules.

Usage:
Functions defined at the top of the file or in a conftest.py module using the
pytest_funcargs__<identifier>
naming scheme will make the <identifier> variable available to be passed as
an argument into individual test functions. The funcarg is created afresh
for every individual test function.
The 'request' parameter provides some useful methods and attributes to modify
the funcarg's behavior. The 'module', 'cls' and 'function' attributes allow us
to see which  test is requesting the funcarg. The 'config' attribute allows
us to check the command-line arguments and other config data.
The 'addfinalizer' method allows us  to do additonal cleanup on the funcarg.
'''
from stats_list import StatsList


def pytest_funcargs__valid_stats(request):
    return StatsList([1,2,2,3,3,4])


def test_mean(valid_stats):
    assert valid_stats.mean() == 2.5


def test_median(valid_stats):
    assert valid_stats.median() == 2.5
    valid_stats.append(4)
    assert valid_stats.median() == 3


def test_mode(valid_stats):
    assert valid_stats.mode() == [2, 3]
    valid_stats.remove(2)
    assert valid_stats.mode() == [3]

