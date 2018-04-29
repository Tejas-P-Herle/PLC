"""Test class for PLC.py"""
import unittest
#from StringIO import StringIO


class TestPLC(unittest.TestCase):
    def test_main(self):
        """Tests main method of PLC"""

        # Create test set with valid data
        valid_test_set = [
            ("test_examples/python_file_1.py", "JaVA", "java.java"),
            ("test_examples/java_file_1.java", "CpP", "cpp.cpp"),
            ("test_examples/cpp_file_1.cpp", "C", "c.c"),
            ("test_examples/c_file_1.c", "PytHOn", "python.py"),
        ]
 
        # Create test set with invalid
        #unsupported_test_set = [
        #    "Unsupported_file_type.abc",
        #    "Unsupported_random_file_type.random",
        #    "Unsupported_num_file.123",
        #    "\x03.hex",
        #]

        # Create test set for invalid types
        #invalid_type_test_set = [
        #    1234,
        #    b'python_file.py',
        #]

        # Add expected results
        #for i, test in enumerate(unsupported_test_set):
        #    unsupported_test_set[i] = (
        #        test,
        #        unsupported_error.format(path.splitext(test)[1])
        #    )
        
        #for i, test in enumerate(invalid_type_test_set):
        #    invalid_type_test_set[i] = (test, invalid_type_error)

        # Merge invalid test sets
        #invalid_test_set = unsupported_test_set + invalid_type_test_set
        
        # Merge both test sets
        #test_set = valid_test_set + invalid_test_set

        # Run test for all tests in test_set
        #for test in test_set:
        #    self.assertEqual(Language.recognize(test[0]), test[1])
