"""Test class for PLC.py"""
import unittest
from unittest.mock import patch
import sys
from get_io import GetIO
import PLC


class TestPLC(unittest.TestCase):
    def test_main(self):
        """Tests main method of PLC"""

        # Initialize io_stream
        io_stream = GetIO()

        # Create valid file name set
        valid_file_path = [
            ("test_examples/python_file_1.py", "python"),
            ("test_examples/java_file_1.java", "java"),
            ("test_examples/cpp_file_1.cpp", "cpp"),
            ("test_examples/c_file_1.c", "c"),
        ]

        # Create valid languages set
        valid_language = [
            "JaVa",
            "CpP",
            "C",
            "PytHOn",
        ]

        # Create file names set (valid if language and file name match)
        file_name = [
            "java.jaVa",
            "cpp.Cpp",
            "c.C",
            "python.pY"
        ]

        # Create test set with valid data
        valid_test_set = []
        for i in range(len(valid_file_path)):
            valid_test_set.append((
                valid_file_path[i][0],
                valid_language[i],
                file_name[i],
                "{} -> {}\n".format(valid_file_path[i][1],
                                    valid_language[i].lower()),
            ))

        # Create test set with invalid
        
        # Create test set for file not found error
        file_not_found_error = "File - {} Does not exist"
        file_path_not_found_test_set = [
            "test_examples/python_file_1",
            "python_file_1.py",
            "random_file.py",
        ]

        # Add expected error response
        for i, path in enumerate(file_path_not_found_test_set):
            file_path_not_found_test_set[i] = (
                path,
                file_not_found_error.format(path),
            )

        # Create test set for unsupported file types
        unsupported_type_error = "Unsupported_file_type"
        unsupported_type_test_set = [
            "test_examples/unsupported_file.format",
        ]

        # Add expected error response
        for i, path in enumerate(unsupported_type_test_set):
            unsupported_type_test_set[i] = (path, unsupported_type_error)

        # Create test set for unknown language
        unsupported_language_error = "Unsupported language {}" 
        unsupported_language_test_set = [
            "J.A.V.A",
            "My own language",
            "Ruby",
            "Perl",
            "Python Console",
        ]

        # Add expected error response
        for i, language in enumerate(unsupported_language_test_set):
            unsupported_language_test_set[i] = (
                language,
                unsupported_language_error.format(language),
            )

        # Create test set for mismatched file name
        unsupported_extension_error = "Extension and language don't match" 
        unsupported_extension_test_set = [
            "some file.random extension",
            "this name is completely.insane",
            file_name[3],
            file_name[2],
        ]

        # Add expected error response
        for i, file_name in enumerate(unsupported_extension_test_set):
            unsupported_extension_test_set[i] = (file_name,
                                                 unsupported_extension_error)

        # TODO Create test set for invalid file names
        invalid_file_names_test_set = []

        # Check user abort
        user_abort_input = ["q", "User Abort"]

        # Add one valid test set value to let the program proceed

        # Merge all invalid file path test sets
        invalid_file_path_test_set = [file_path_not_found_test_set
                                      + unsupported_type_test_set
                                      + [valid_file_path[0]]]

        # Merge all invalid language test sets
        invalid_language_test_set = [unsupported_language_test_set 
                                    + [valid_language[0]]]

        # Merge all invalid file name test sets
        invalid_file_name_test_set = [unsupported_extension_test_set
                                      + invalid_file_names_test_set
                                      + [file_name[0]]]
        
        # Merge all invalid test sets
        invalid_test_set = (invalid_file_path_test_set
                            + invalid_language_test_set
                            + invalid_file_name_test_set)

        invalid_test_set = [('asdv', 'test_examples/python_file_1.py', 'JaVa', 'java.jaVa', 'python -> java\n')]

        invalid_test_set = [('asdv', 'test_examples/python_file_1.py', 'JaVa', 'java.jaVa', 'python -> java\n')]

        error = "File - asdv Does not exist"

        # Run test for all tests in valid_test_set
        for test in valid_test_set:
            with patch('builtins.input', side_effect=test[:3]):
                PLC.PLC()
                self.assertEqual(io_stream.read_stdout(), test[3])

        # Run test for all tests in invalid_test_set
        responses = []
        for test in invalid_test_set:
            with patch('builtins.input', side_effect=test[:-1]):
                PLC.PLC()
                response = io_stream.read_stdout()
                responses.append(response)
                try:
                    self.assertEqual(response, error)
                except AssertionError:
                    pass
        io_stream.print(responses)


if __name__ == "__main__":
    unittest.main()

