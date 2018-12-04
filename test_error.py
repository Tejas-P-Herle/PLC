"""Tests Error Class"""
import unittest
from error import Error

from logger import Logger

LOG_FILE = "PLC_log.log"
logger = Logger("test_error")


class TestError(unittest.TestCase):
    def test_parse(self):
        
        # Create test_cases
        test_cases = [
            "Valid Error Message",
            b"Invalid Error Message",
            123,
            "\x03"
        ]

        # Store expected logging messages
        log_lines = []
        for test in test_cases:
            log_lines.append("error - E - " + str(test))
        
        # For test in test_cases, test if functions as expected
        for test in test_cases:
            self.assertEqual(Error.parse(test), None)
        
        # Check if messages are logged in file
        with open(LOG_FILE, "r+") as file:
            
            # Read lines from file
            file_lines = [line.strip("\n") for line in file.readlines()]
            
            # Count number of lines
            number_of_lines = len(file_lines)
            
            # Check if number of lines is greater than 4
            self.assertTrue(number_of_lines >= 4)

            # Get lines logged by testing
            logged_lines = [" - ".join(line.split(" - ")[1:])
                for line in file_lines[number_of_lines - 4:]]
            
            # Check if all lines are logged properly
            for line in log_lines:
                self.assertTrue(line in logged_lines)

            # Delete all logged lines
            file_lines = file_lines[:number_of_lines - 4]
            
            # Truncate file
            file.truncate(0)
            file.seek(0)
            
            # Write all modified lines
            file.write("\n".join(file_lines) + "\n")


if __name__ == "__main__":
    unittest.main()
