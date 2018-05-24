"""Tests file_path.FilePath"""
import unittest
from languages.python import Python


class TestPython(unittest.TestCase):
    def test_replace_logical_ops(self):
        """Tests FilePath.validate_file_name"""

        # Create test set for function
        test_set = [
            "and_str and or_str or not_str and not and_or_not_str",
            "name and uid or reg_no and not unknown and not(std < 1)",
            "&&_str && ||_str || n!_str && u! &&_||_!_str"
        ]

        # Create expected results test set for function
        res_set = [
            "and_str && or_str || not_str && !and_or_not_str",
            "name && uid || reg_no && !unknown && !(std < 1)",
            "&&_str and ||_str or n!_str and u! &&_||_!_str"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test from conversion
            self.assertEqual(Python().replace_logical_ops(test_set[i], "to"),
                             res_set[i])

            # Test to conversion
            self.assertEqual(Python().replace_logical_ops(res_set[i], "from"),
                             test_set[i])


if __name__ == "__main__":
    unittest.main()
