"""Tests file_path.FilePath"""
import unittest
from file_path import FilePath


class TestFilePath(unittest.TestCase):
    def test_validate_file_path(self):
        """Tests FilePath.validate_file_path"""
        
        # Create test set with valid data
        valid_test_set = [
            ("test_examples/python_file_1.py", None),
            ("test_examples/java_file_1.java", None), 
            ("test_examples/cpp_file_1.cpp", None),
            ("test_examples/c_file_1.c", None)
        ]

        # Create test set with invalid data

        # Define error string
        error_str = "File - {} Does not exist"
       
        # Create list of invalid file paths
        file_paths = [
            "python_file_1.py",
            "test_examsples/c_file_1",
            "abcdef.c",
            "1234-?/!__.;:'\""
        ]

        # Add expected results
        invalid_test_set = []

        for file_path in file_paths:
            invalid_test_set.append((file_path, error_str.format(file_path)))

        # Merge both test sets
        test_set = valid_test_set + invalid_test_set
 
        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(FilePath.validate_file_path(test[0]), test[1])

    def test_validate_file_name(self):
        """Tests FilePaht.validate_file_name"""

        # Create test set with valid data
        valid_test_set = [
            
        ]

        # Create test set with invalid data
        invalid_test_set = [

        ]

        # Merge both test sets
        test_set = valid_test_set + invalid_test_set
        
        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(FilePath.validate_file_path(*test[:2]), test)


if __name__ == "__main__":
    unittest.main()
