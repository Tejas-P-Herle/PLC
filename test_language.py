"""Tests language.Language class"""
import unittest
from language import Language
from os import path


class TestLanguage(unittest.TestCase):
    def test_get_language(self):
        """Tests Language.get_language"""
        
        # Create test set with valid data
        valid_test_set = [
            (".py", "python"),
            (".java", "java"),
            (".cpp", "cpp"),
            (".c", "c"),
            (u".java", "java"),
            (".JaVa", "java"),
            (".JAVA", "java"),
        ]

        # Create test set with invalid data
        unsupported_error = "Unsupported file extension {}"
        invalid_type_error = "Parameter extension must be a string"
        
        # Create test set with unsupported extensions
        unsupported_test_set = [
            ".rand",
            "blah",
            ".1234",
            "\x03",
        ]

        # Create test set with invalid types
        invalid_type_test_set = [
            1234,
            b".py",
        ]

        # Add expected response
        for i, test in enumerate(unsupported_test_set):
            unsupported_test_set[i] = (test, (None, unsupported_error.format(test)))

        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] = (test, (None, invalid_type_error))

        # Merge invalid test sets
        invalid_test_set = unsupported_test_set + invalid_type_test_set

        # Merge both test sets
        test_set = valid_test_set + invalid_test_set

        # Function to test if correct response
        is_correct = lambda result, test: result.startswith(test[1])

        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(Language.get_language(test[0]), test[1])
    
    def test_recognize(self):
        """Tests Language.recognize"""

        # Create test set with valid data
        valid_test_set = [
            "python_file.py",
            "java_file.java",
            "cpp_file.cpp",
            "c_file.c",
            "java_file.JAVA",
            "java_file.JaVa",
            "python_\x09.py",
        ]

        # Add expected response
        for i, test in enumerate(valid_test_set):
            valid_test_set[i] = (test, test.split('_')[0].lower())

        # Create test set with invalid date
        unsupported_error = "Unsupported file extension {}"
        invalid_type_error = "Parameter file_path must be a string"
        
        # Create test set for unsupported languages
        unsupported_test_set = [
            "Unsupported_file_type.abc",
            "Unsupported_random_file_type.random",
            "Unsupported_num_file.123",
            "\x03.hex",
        ]

        # Create test set for invalid types
        invalid_type_test_set = [
            1234,
            b'python_file.py',
        ]

        # Add expected results
        for i, test in enumerate(unsupported_test_set):
            unsupported_test_set[i] = (
                test,
                (None, unsupported_error.format(path.splitext(test)[1]))
            )
        
        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] = (test, (None, invalid_type_error))

        # Merge invalid test sets
        invalid_test_set = unsupported_test_set + invalid_type_test_set
        
        # Merge both test sets
        test_set = valid_test_set + invalid_test_set

        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(Language.recognize(test[0]), test[1])


    def test_validate(self):
        """Tests Language.validate"""
        
        # Create test set with valid data
        valid_test_set = [
            "python",
            "java",
            "cpp",
            "c",
            u"java",
            "JAVA",
        ]

        # Add expected response
        valid_return_value = None
        for i, test in enumerate(valid_test_set):
            valid_test_set[i] = (test, valid_return_value)

        # Create test set with invalid data
        unsupported_error = "Unsupported language {}"
        invalid_type_error = "Parameter language must be a string"
        
        # Create test set with unsupported languages
        unsupported_test_set = [
            "rand",
            "blah",
            "1234",
            ".py",
            "python_",
            "\x03",
        ]

        # Create test set with invalid type
        invalid_type_test_set = [
            1234,
            b"java",
        ]

        # Add expected results
        for i, test in enumerate(unsupported_test_set):
            unsupported_test_set[i] = (test, unsupported_error.format(test))

        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] = (test, invalid_type_error.format(test))

        # Merge invalid test sets
        invalid_test_set = unsupported_test_set + invalid_type_test_set

        # Merge valid test sets
        test_set = valid_test_set + invalid_test_set

        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(Language.validate(test[0]), test[1])


if __name__ == '__main__':
    unittest.main()
