"""Tests language.Language class"""
import unittest
from language import Language


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
            (".JAVA", "java")
        ]

        # Create test set with invalid data
        unsupported_error = "Unsupported file extension {}"
        invalid_test_set = [
            (".rand", unsupported_error),
            ("blah", unsupported_error),
            (".1234", unsupported_error),
            (1234, unsupported_error),
            (b".py", unsupported_error),
            ("\x03", unsupported_error)
        ]

        # Merge both test sets
        test_set = valid_test_set + invalid_test_set

        # Function to test if correct response
        is_correct = lambda result, test: result.startswith(test[1])

        # Run test for all tests in test_set
        for test in test_set:
            self.assertTrue(is_correct(Language.get_language(test[0]), test))
    
    def test_recognize(self):
        """Tests Language.recognize"""

        # Create test set with valid data
        valid_test_set = [
            "python_file.py",
            "java_file.java",
            "cpp_file.cpp",
            "c_file.c",
            "java_file.JAVA",
            "java_file.JaVa"
        ]

        # Create test set with invalid date
        invalid_test_set = [
            "Unsupported_file_type.abc",
            "Unsupported_random_file_type.random",
            "Unsupported_num_file.123"
        ]
        
        # Merge both test sets
        test_set = valid_test_set + invalid_test_set

        # Function to test if correct response
        is_correct = lambda result, test: result.startswith(test.split('_')[0])
        
        # Run test for all tests in test_set
        for test in test_set:
            self.assertTrue(is_correct(Language.recognize(test), test))


    def test_validate(self):
        """Tests Language.validate"""
        
        # Define expected value on validity of language
        valid_return_value = None

        # Create test set with valid data
        valid_test_set = [
            ("python", valid_return_value),
            ("java", valid_return_value),
            ("cpp", valid_return_value),
            ("c", valid_return_value),
            (u"java", valid_return_value),
            ("JAVA", valid_return_value)
        ]

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
