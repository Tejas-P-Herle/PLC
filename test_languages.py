"""Runs all test files for all classes"""
import unittest
from languages.test_python import TestPython

test_cases = tuple([TestPython])


def load_tests():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for test_class in test_cases:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(load_tests())
