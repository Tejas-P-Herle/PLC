"""Test class for PLC.py"""
import unittest
from unittest.mock import patch
import sys
from get_io import GetIO
import PLC


class TestPLC(unittest.TestCase):
    def test_PLC(self):
        """Tests PLC function of file PLC.py"""

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
        file_path_not_found_test_set = (
            "test_examples/python_file_1",
            "python_file_1.py",
            "random_file.py",
        )

        # Store expected error response
        file_not_found_expected_error = []
        for path in file_path_not_found_test_set:
            error_string = file_not_found_error.format(path)
            file_not_found_expected_error.append(error_string)

        # Create test set for unsupported file types
        unsupported_type_error = "Unsupported file type"
        unsupported_type_test_set = (
            "test_examples/unsupported_file.format",
        )

        # Store expected error response
        test_size = len(unsupported_type_test_set)
        unsupported_type_expected_error = [unsupported_type_error] * test_size

        # Create test set for unknown language
        unsupported_language_error = "Unsupported language {}" 
        unsupported_language_test_set = (
            "J.A.V.A",
            "My own language",
            "Ruby",
            "Perl",
            "Python Console",
        )

        # Store expected error response
        unsupported_language_expected_error = []
        for i, language in enumerate(unsupported_language_test_set):
            error_string = unsupported_language_error.format(language)
            unsupported_language_expected_error.append(error_string)

        # Create test set for mismatched file name
        unsupported_extension_error = "Extension and language don't match" 
        unsupported_extension_test_set = (
            "some file.random extension",
            "this name is completely.insane",
            file_name[3],
            file_name[2],
        )

        # Store expected error response
        test_size = len(unsupported_extension_test_set)
        unsupported_extension_expected_error = ([unsupported_extension_error]
                                                 * test_size)

        # Create test set for invalid file names
        invalid_file_name_error = "File name must not contain '\\/:*?\"<>|'"
        invalid_file_name_test_set = (
            "java_file/\\\"Epic:<*|*>?\".java",
            "file\\my\\path.py"
        )

        # Store expected error response
        invalid_file_name_expected_error = ([invalid_file_name_error]
                                            * len(invalid_file_name_test_set))

        # Check user abort
        user_abort = ("q", "User Abort")

        # Add one valid test set value to let the program proceed

        # Merge all invalid file path test sets
        invalid_file_path_test_set = (file_path_not_found_test_set
                                      + unsupported_type_test_set
                                      + tuple([valid_file_path[0][0]]))

        # Merge all file path related expected errors
        file_path_expected_error = (file_not_found_expected_error
                                    + unsupported_type_expected_error
                                    + [""])

        # Merge all invalid language test sets
        invalid_language_test_set = (unsupported_language_test_set 
                                    + tuple([valid_language[0]]))
        
        # Merge all language related expected errors
        language_expected_error = (unsupported_language_expected_error
                                   + [""])

        # Merge all invalid file name test sets
        invalid_file_name_test_set = (unsupported_extension_test_set
                                      + invalid_file_name_test_set
                                      + tuple([file_name[0]]))
        
        # Merge all file name related expected errors
        valid_input_result = "{} -> {}\n".format(valid_file_path[0][1],
                                                 valid_language[0].lower())
        file_name_expected_error = (unsupported_extension_expected_error
                                    + invalid_file_name_expected_error
                                    + [valid_input_result])
        
        # Merge all invalid test sets
        invalid_test_set = (invalid_file_path_test_set
                            + invalid_language_test_set
                            + invalid_file_name_test_set)
        
        # Merge all expected error lists
        expected_error = ("\n\n".join(file_path_expected_error)
                          + "\n\n".join(language_expected_error)
                          + "\n\n".join(file_name_expected_error))

        # Run test for all tests in valid_test_set
        for test in valid_test_set:
            with patch('builtins.input', side_effect=test[:3]):
                PLC.PLC()
                self.assertEqual(io_stream.read_stdout(), test[3])

        # Run test for all tests in invalid_test_set
        io_stream.reset_stdout_line_count()
        with patch('builtins.input', side_effect=invalid_test_set):
            PLC.PLC()
            self.assertEqual(io_stream.read_stdout(), expected_error)

        # Run test for user abort function
        with patch('builtins.input', return_value=user_abort[0]):
            with self.assertRaises(SystemExit):
                PLC.PLC()
                self.assertEqual(io_stream.read_stdout(), user_abort[1])


if __name__ == "__main__":
    unittest.main()

