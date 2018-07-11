"""Runs all test files for all classes"""
import unittest
from languages.test_python import TestPython
from languages.test_java import TestJava
from languages.test_cpp import TestCPP
from languages.test_c import TestC

test_cases = tuple([TestJava, TestPython, TestCPP, TestC])


def load_tests():
    # Load test suite
    suite = unittest.TestSuite()

    # Load test loader
    loader = unittest.TestLoader()

    # Iterate over test cases
    for test_class in test_cases:
        
        # Load all tests from test classes
        tests = loader.loadTestsFromTestCase(test_class)

        # Add test to test suite
        suite.addTests(tests)

    # Return test suite
    return suite


if __name__ == '__main__':
    # Load text for of test runner
    runner = unittest.TextTestRunner()
    
    # Run all tests in all test classes
    runner.run(load_tests())
