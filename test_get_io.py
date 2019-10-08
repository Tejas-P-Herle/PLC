import unittest
from get_io import GetIO
import sys
from io import StringIO
from random import random


class TestGetIO(unittest.TestCase):
    default_stdout, default_stderr = sys.stdout, sys.stderr

    def test___init__(self):
        """Test case for GetIO.__init__"""

        # Define expected result list
        res_tup = (self.default_stdout, self.default_stderr,
                   True, True, False, 0, 0)
        
        # Initiate class
        iostream = GetIO()

        # Check function output
        self.assertEqual(
            (iostream.default_stdout, iostream.default_stderr,
            isinstance(sys.stdout, StringIO), isinstance(sys.stderr, StringIO),
            iostream.reset, iostream.stdout_line_count,
            iostream.stderr_line_count),
            res_tup
        )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        
    def test_stub_output(self):
        """Test case for GetIO.stub_output"""
        
        # Define expected result list
        res_tup = (True, True, False)

        # Initiate class
        iostream = GetIO()

        # Run method
        iostream.stub_output()

        # Check function output
        self.assertEqual(
            (isinstance(sys.stdout, StringIO), isinstance(sys.stderr, StringIO),
            iostream.reset),
            res_tup
        )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        
        
    def test_reset_output(self):
        """Test case for GetIO.reset_output"""

        # Define expected result list
        res_tup = (self.default_stdout, self.default_stderr, True)

        # Initiate class
        iostream = GetIO()

        # Run method
        iostream.reset_output()

        # Check function output
        self.assertEqual(
            (sys.stdout, sys.stderr, iostream.reset),
            res_tup
        )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        
    def test_read_stdout(self):
        """Test case for GetIO.read_stdout"""

        # Define test text list
        test_texts = [
            "Test Text 1",
            "Numbers 1234",
            "Special characters !@#$%^&*(){}+=-[]",
            "Function characters "
        ]

        # Initiate class
        iostream = GetIO()

        # Iterate over test texts
        for text in test_texts:

            # Print test text
            print(text)

            # Run method
            res = iostream.read_stdout()

            # Check function output
            self.assertEqual(
                res, text + "\n"
            )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        
    def test_read_stderr(self):
        """Test case for GetIO.read_stderr"""

        # Define test text list
        test_texts = [
            "Test Text 1",
            "Numbers 1234",
            "Special characters !@#$%^&*(){}+=-[]",
            "Function characters "
        ]

        # Initiate class
        iostream = GetIO()

        # Iterate over test texts
        for text in test_texts:

            # Print test text
            print(text, file=sys.stderr)

            # Run method
            res = iostream.read_stderr()

            # Check function output
            self.assertEqual(
                res, text + "\n"
            )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        
    def test_read_output(self):
        """Test case for GetIO.read_output"""

        # Define test text list
        test_texts = [
            "Test Text 1",
            "Numbers 1234",
            "Special characters !@#$%^&*(){}+=-[]",
            "Function characters "
        ]

        # Initiate class
        iostream = GetIO()

        # Iterate over test texts
        for text in test_texts:

            # Randomly select stderr or stdout
            if random() < 0.5:

                # Print test text
                print(text)

            else:
                
                # Print test text to stderr
                print(text, file=sys.stderr)

            # Run method
            res = [text for text in iostream.read_output() if text][0]

            # Check function output
            self.assertEqual(
                res, text + "\n"
            )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        
    def test_print(self):
        """Test case for GetIO.print"""

        # Define test text list
        test_texts = [
            "Test Text 1",
            "Numbers 1234",
            "Special characters !@#$%^&*(){}+=-[]",
            "Function characters "
        ]

        # Initiate class
        iostream = GetIO()

        # Iterate over test texts
        for text in test_texts:

            # Initiate StringIO object and stub default stdout
            buffer = StringIO()
            iostream.default_stdout = buffer

            # Print to console
            iostream.print(text)
            iostream.default_stdout = self.default_stdout

            # Read stdout
            res = buffer.getvalue()

            # Check function output
            self.assertEqual(
                (res, isinstance(sys.stdout, StringIO)), (text + "\n", True)
            )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        
    def test_reset_stdout_line_count(self):
        """Test case for GetIO.reset_stdout_line_count"""

        # Create StringIO instance
        iostream = GetIO()

        # Run method
        iostream.reset_stdout_line_count()

        # Test function with inputs and expected outputs
        self.assertEqual(
            iostream.stdout_line_count, 0
        )

        # Reset stdout and stderr
        sys.stdout, sys.stderr = self.default_stdout, self.default_stderr
        

if __name__ == '__main__':
    unittest.main()
