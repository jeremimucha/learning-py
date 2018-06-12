import sys
import py.test


def test_simple_skip():
    if sys.platform != 'fakeos':
        py.test.skip("Test works only on fakeOS")

    fakeos.do_something_fake()
    assert fakeos.did_not_happen


@py.test.mark.skipif('sys.version_info <= (3,0)')
def test_python3():
    assert b'hello'.decode() == 'hello'
