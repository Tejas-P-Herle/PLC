"""Runs all test files for all classes"""
import unittest
from test_language import TestLanguage
from test_file_path import TestFilePath
from test_error import TestError
from test_PLC import TestPLC
from languages.test_python import TestPython

test_cases = (TestPLC, TestLanguage, TestFilePath, TestError, TestPython)


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
