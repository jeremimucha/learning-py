#! /usr/bin/env python


def test_true():
    assert True


def test_false():
    assert False


# Reported failures are readable
def test_key():
    a = ['a', 'b']
    b = ['b']
    assert a == b

