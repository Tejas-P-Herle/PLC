"""Tests Error Class"""
import unittest
from error import Error


class TestError(unittest.TestCase):
    def test_parse(self):
        
        # Create test_cases
        test_cases = [
            "Valid Error Message",
            b"Invalid Error Message",
            123,
            "\x03"
        ]
        
        # For test in test_cases, test if functions as expected
        for test in test_cases:
            self.assertEqual(Error.parse(test), None)


if __name__ == "__main__":
    unittest.main()
