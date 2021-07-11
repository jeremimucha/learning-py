from unittest import mock


def test_basic_mock():
    m = mock.Mock()
    m.some_attribute = "hello world"
    m.some_method.return_value = 42

    print(m.some_attribute)
    print(m.some_method('with', 'arguments'))


# Mocks may have side effects - arbitrary functions may be assigned to members

def test_mock_side_effects():
    m = mock.Mock()
    def print_hello(*args):
        print('Hello, World!')
        return 43

    m.some_method.side_effect = print_hello
    print(m.some_method())
    print(m.some_method.call_count)

    m.some_method('foo', 'bar')
    m.some_method.assert_called_once_with('foo', 'bar')
    m.some_method.assert_called_once_with('foo', mock.ANY)
    m.some_method.assert_called_once_with('foo', 'baz')


# Replacing a function/method/object from an external module
import os

def test_mock_patching():
    def fake_os_unlink(path):
        raise IOError("Testing")

    with mock.patch('os.unlink', fake_os_unlink):
        os.unlink('foobar')


# mock.patch can replace any part of an external piece of code
import requests
import pytest


class WhereIsPythonError(Exception):
    pass


def is_python_still_a_programming_language():
    try:
        r = requests.get("https://python.org")
    except IOError:
        pass
    else:
        if r.status_code == 200:
            return 'Python is a programming language' in r.content
        raise WhereIsPythonError("Something bad happened")


def get_fake_get(status_code, content):
    m = mock.Mock()
    m.status_code = status_code
    m.content = content

    def fake_get(url):
        return m
    
    return fake_get

def raise_get(url):
    raise IOError("Unable to fetch url %s" % url)


@mock.patch('requests.get', get_fake_get(200, 'Python is a programming language for sure'))
def test_python_is():
    assert is_python_still_a_programming_language() is True

@mock.patch('requests.get', get_fake_get(200, 'Python is no more a programming language'))
def test_python_is_not():
    assert is_python_still_a_programming_language() is False

@mock.patch('requests.get', get_fake_get(404, 'Whatever'))
def test_bad_status_code():
    with pytest.raises(WhereIsPythonError):
        is_python_still_a_programming_language()

@mock.patch('requests.get', raise_get)
def test_ioerror():
    with pytest.raises(WhereIsPythonError):
        is_python_still_a_programming_language()
