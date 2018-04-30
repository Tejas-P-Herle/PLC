"""Tests file_path.FilePath"""
import unittest
from file_path import FilePath


class TestFilePath(unittest.TestCase):
    def test_validate_file_path(self):
        """Tests FilePath.validate_file_path"""
        
        # Create test set with valid data
        valid_test_set = [
            "test_examples/python_file_1.py",
            "test_examples/java_file_1.java", 
            "test_examples/cpp_file_1.cpp",
            "test_examples/c_file_1.c",
        ]

        # Add expected results
        valid_test_return_value = None
        for i, test in enumerate(valid_test_set):
            valid_test_set[i] = (test, valid_test_return_value)

        # Define error string
        invalid_file_path_error_str = "File - {} Does not exist"
        invalid_type_error = "Parameter file_path must be a string"
       
        # Create list of invalid file paths
        invalid_file_path_test_set = [
            "python_file_1.py",
            "test_examsples/c_file_1",
            "abcdef.c",
            "1234-?/!__.;:'\"",
        ]

        # Create test set of invalid type
        invalid_type_test_set = [
            b"test_examples/python_file_1.py",
            123,
        ]

        # Add expected results
        for i, file_path in enumerate(invalid_file_path_test_set):
            invalid_file_path_test_set[i] = (
                file_path,
                invalid_file_path_error_str.format(file_path),
            )
        
        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] = (test, invalid_type_error)

        # Merge invalid test sets
        invalid_test_set = invalid_file_path_test_set + invalid_type_test_set

        # Merge both test sets
        test_set = valid_test_set + invalid_test_set
 
        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(FilePath.validate_file_path(test[0]), test[1])

    def test_validate_file_name(self):
        """Tests FilePath.validate_file_name"""

        # Create test set with valid data
        valid_test_set = [
            ("python_file_1.py", "python"),
            ("java_file_1.java", "java"), 
            ("cpp_file_1.cpp", "cpp"),
            ("c_file_1.c", "c"),
        ]

        # Add expected results
        valid_test_return_value = None
        for i, test in enumerate(valid_test_set):
            valid_test_set[i] += tuple([valid_test_return_value])

        # Define error string
        mismatch_file_name_error = "Extension and language don't match"
        parameters = "file_name and input_language"
        invalid_file_name_error = "File name must not contain '\\/:*?\"<>|'"
        invalid_type_error = "Parameters %s must be a string" % parameters
       
        # Create list of invalid file paths
        mismatch_file_name_test_set = [
            ("python_file_1.py", "java"),
            ("test_examples_c_file_1", "c"),
            ("abcdef.c", "python"),
        ]

        # Create invalid file_name test set
        invalid_file_name_test_set = [
            ("random|file.extension", "python"),
            ("completely_|nvalid<>\\/:*?\".java", "java")
        ]

        # Create test set of invalid type
        invalid_type_test_set = [
            (b"test_examples/python_file_1.py", 123),
            (123, "python"),
            ("rand.py", b"python"),
        ]

        # Add expected results
        for i, file_path in enumerate(mismatch_file_name_test_set):
            mismatch_file_name_test_set[i] += tuple([mismatch_file_name_error])

        for i, file_name in enumerate(invalid_file_name_test_set):
            invalid_file_name_test_set[i] += tuple([invalid_file_name_error])
        
        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] += tuple([invalid_type_error])

        # Merge invalid test sets
        invalid_test_set = (mismatch_file_name_test_set
                            + invalid_file_name_test_set
                            + invalid_type_test_set)
        
        # Merge both test sets
        test_set = valid_test_set + invalid_test_set
 
        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(FilePath.validate_file_name(*test[:2]), test[2])


if __name__ == "__main__":
    unittest.main()
