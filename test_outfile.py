"""Test output of PLC on different test files"""

import unittest
from PLC import PLC
from os import path
from unittest.mock import patch

from get_io import GetIO


class TestOutfile(unittest.TestCase):
    @staticmethod
    def get_output(input_file, lang_to, outfile_name):
        """Returns PLC output for given input parameters"""
        
        # Set file overwrite to true
        overwrite = "Y"

        # Make list of all inputs
        input_list = [
            input_file,
            lang_to,
            outfile_name,
            overwrite
        ]

        # Make GetIO object (to stub input)
        io_stream = GetIO()

        # Stub input
        with patch("builtins.input", side_effect=input_list):

            # Stub output to StringIO
            io_stream.stub_output()

            # Run PLC with parameters
            PLC()

            # Reset output to standard output
            io_stream.reset_output()

            # Open output file
            with open(outfile_name) as file:

                # Read and return lines from output file
                return [line.strip() for line in file.readlines() if line.strip() != ""]
    
    def test_python_1(self):
        """Test Case for file - test_exampes/python_1.py"""

        # Set input parameters
        input_file = "test_examples/python_1.py"
        lang_to = "java"
        outfile_name = "test_examples/python_1_outfile.java"

        # Set expected ouput
        expected_output = [line.strip() for line in """
        class Python_1_Outfile {
            public static void main(String[] args) {
                System.out.println("Hello World\\n");
            }
        }""".split("\n") if line.strip() != ""]

        # Get PLC ouput
        PLC_output = self.get_output(
            input_file,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual(expected_output,
                         [line.strip() for line in PLC_output])


    def test_python_2(self):
        """Test Case for file - test_exampes/python_2.py"""

        # Set input parameters
        input_file = "test_examples/python_2.py"
        lang_to = "java"
        outfile_name = "test_examples/python_2_outfile.java"

        # Set expected ouput
        expected_output = [line.strip() for line in """
        class Python_2_Outfile {
            public static void main(String[] args) {
                int value = 1;
                if (value == 0) {
                    System.out.println("False");
                }
                else if (value == 1) {
                    System.out.println("True");
                }
                else {
                   System.out.println("Undefined");
                }
            }
        }""".split("\n") if line.strip() != ""]

        # Get PLC ouput
        PLC_output = self.get_output(
            input_file,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual(expected_output,
                         [line.strip() for line in PLC_output])

    def test_python_3(self):
        """Test Case for file - test_exampes/python_3.py"""

        # Set input parameters
        input_file = "test_examples/python_3.py"
        lang_to = "java"
        outfile_name = "test_examples/python_3_outfile.java"

        # Set expected ouput
        expected_output = [line.strip() for line in """
        class Python_3_Outfile {
            public static void main(String[] args) {
                int j = 0;
                for (int i = 0; i < 10; i++) {
                    j += i;
                System.out.println(i.toString() + j.toString());
                }
            }
        }""".split("\n") if line.strip() != ""]

        # Get PLC ouput
        PLC_output = self.get_output(
            input_file,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual(expected_output,
                         [line.strip() for line in PLC_output])


    def test_python_4(self):
        """Test Case for file - test_exampes/python_4.py"""

        # Set input parameters
        input_file = "test_examples/python_4.py"
        lang_to = "java"
        outfile_name = "test_examples/python_4_outfile.java"

        # Set expected ouput
        expected_output = [line.strip() for line in """
        class Python_4_Outfile {
            public static void main(String[] args) {
                System.out.println("Ends with '!'!");
            }
        }""".split("\n") if line.strip() != ""]

        # Get PLC ouput
        PLC_output = self.get_output(
            input_file,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual(expected_output,
                         [line.strip() for line in PLC_output])

if __name__ == "__main__":
    unittest.main()