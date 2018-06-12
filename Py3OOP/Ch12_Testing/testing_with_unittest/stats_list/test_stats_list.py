'''
unittest module:
setUp method - called before every 'test_*' method - this makes setting up state
before every step require less boilerplate code.

The unittest module offers a 'discover' method - it can be used to run all
tests in current folder and all sub folders. Usage:
py -3 -m unittest discover
This will run all tests in files named 'test_<something>.py'
'''
from stats_list import StatsList
import unittest


class TestValidInputs(unittest.TestCase):
    def setUp(self):
        self.stats = StatsList([1,2,2,3,3,4])

    def test_mean(self):
        self.assertEqual(self.stats.mean(), 2.5)

    def test_median(self):
        self.assertEqual(self.stats.median(), 2.5)
        self.stats.append(4)
        self.assertEqual(self.stats.median(), 3)

    def test_mode(self):
        self.assertEqual(self.stats.mode(), [2,3])
        self.stats.remove(2)
        self.assertEqual(self.stats.mode(), [3])


if __name__ == '__main__':
    unittest.main()
