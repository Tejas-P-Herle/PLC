"""Runs all test files for all classes"""
import unittest
from test_language import TestLanguage
from test_file_path import TestFilePath
from test_error import TestError
from test_PLC import TestPLC
from test_code_processor import TestCodeProcessor
from test_logger import TestLogger
from test_regex_gen import TestRegexGen

from languages.test_python import TestPython
from languages.test_java import TestJava
from languages.test_c import TestC
from languages.test_cpp import TestCPP
from test_outfile import TestOutfile

test_languages = (TestPython, TestJava, TestC, TestCPP)
test_cases = ((TestPLC, TestLanguage, TestFilePath, TestRegexGen,
              TestError, TestCodeProcessor, TestLogger, TestOutfile)
              + test_languages)


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
