"""Tests Error Class"""
import unittest
from error import Error

LOG_FILE = "PLC_log.log"


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
        
        # Check if messages are logged in file
        with open(LOG_FILE, "r") as file:
            file_buffer = file.read()
            for test in test_cases:
                self.assertNotEqual(file_buffer.find(str(test)), -1)



if __name__ == "__main__":
    unittest.main()
