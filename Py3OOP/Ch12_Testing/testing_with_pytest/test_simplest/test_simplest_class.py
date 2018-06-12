'''
An example of using a class prefixed with "Test" for grouping test methods
'''


class TestNumbers:
    def test_int_float(self):
        assert 1 == 1.0

    def test_int_str(self):
        assert 1 == '1'
