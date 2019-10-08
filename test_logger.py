import unittest
import logging
import os

from logger import Logger


class TestLogger(unittest.TestCase):
    def test___init__(self):
        """Test case for Logger.__init__"""

        # Create test set
        test_set = [
            tuple(["a"]),
            ("b", "PLC_log.log", "DEBUG", "a"),
            ("c", "PLC_log.log", "ERROR", "w"),
            ("d", "log_output.log", "DEBUG", "A"),
            ("e", "PLC_log.log")
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs

            # Set rewrite to False
            rewrite = False

            # Check if open mode is write
            if len(test_set[i]) == 4 and test_set[i][3] == "w":
                
                # Then store the file
                with open(test_set[i][1]) as file:
                    
                    # Read file
                    file_str = file.read()
                    
                    # Set rewrite file to True
                    rewrite = True

            # Initiate var_logger object
            var_logger = Logger(*test_set[i])

            # If rewrite flag is set to true, then rewrite the file
            if rewrite:
                
                # Open the file
                with open(test_set[i][1], "w") as file:
                    
                    # Write the file
                    file.write(file_str)

            # Define result tuple
            if len(test_set[i]) == 4:
                res_tup = (test_set[i][2].lower(),
                           os.getcwd() + "\\" + test_set[i][1],
                           test_set[i][3].lower())
            elif len(test_set[i]) == 1:
                res_tup = ("debug",
                           os.getcwd() + "\\" + "PLC_log.log",
                           "a")
            elif len(test_set[i]) == 2:
                res_tup = ("debug",
                           os.getcwd() + "\\" + test_set[i][1],
                           "a")
            elif len(test_set[i]) == 3:
                res_tup = (test_set[i][2],
                           os.getcwd() + "\\" + test_set[i][1],
                           "a")

            # Check if attributes are properly set with user input parameters
            self.assertEqual(
                (logging.getLevelName(
                    logging.getLogger(test_set[i][0]).level).lower(),
                 logging.getLogger(test_set[i][0]).handlers[0].baseFilename,
                 logging.getLogger(test_set[i][0]).handlers[0].mode), res_tup
            )

        # Delete test log file
        os.remove("log_output.log")
        
    def test_log(self):
        """Test case for Logger.log"""

        # Create test set
        test_set = [
             tuple(["Debug message"]),
             ("Error message", "error"),
             ("Critical message", "CRITICAL"),
             ("Info message", "iNfO"),
             ("Warning message", "WARning"),
             ("Not Set message", "Not Set"),
             ("Debug message 2", "DEBUG")
        ]
        
        # Create expected results test set
        res_str = "\n".join([line.strip() for line in """
        test_logger - D - Debug message
        test_logger - E - Error message
        test_logger - C - Critical message
        test_logger - I - Info message
        test_logger - W - Warning message
        test_logger - D - Debug message 2
        """.strip().split("\n")])

        # Set omitted messages count
        omitted_msgs = 1
        
        # Initiate plc_logger
        plc_logger = Logger("test_logger")

        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            try:
                # Log all test messages
                plc_logger.log(test_set[i][0], level=test_set[i][1])
            except IndexError:

                # If level is not given, pass only log text
                plc_logger.log(test_set[i][0])
        
        # Test logged messages and verify logged text
        with open(plc_logger.filename, "r+") as file:

            # Read file
            file_lines = file.readlines()

            # Get logged messages start
            log_start = (-1 * (len(test_set)) + omitted_msgs)

            # Start from logged messages start
            lines = file_lines[log_start:]

            # Format lines from file
            lines = "\n".join([" - ".join(
                line.strip().split(" - ")[1:]) for line in lines])

            # Check equality
            self.assertEqual(lines, res_str)

            # Truncate file
            file.truncate(0)
            file.seek(0)

            # Write modified lines
            file.write("".join(file_lines[:log_start]))

        # Delete plc_logger
        del plc_logger

if __name__ == '__main__':
    unittest.main()
