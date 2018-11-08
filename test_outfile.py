"""Test output of PLC on different test files"""

import unittest
from PLC import PLC
from os import path, remove
from unittest.mock import patch
from tempfile import TemporaryFile

from get_io import GetIO


class TestOutfile(unittest.TestCase):
    @staticmethod
    def get_output(file_content, lang_to, outfile_name):
        """Returns PLC output for given input parameters"""

        # Make new temporary file
        with TemporaryFile(delete=False, suffix=".py", dir=".", mode="x+") as file:
            
            # Write test program to file
            file.write("\n".join(file_content))

            # Save file name
            file_name = file.name

            # Seek start of file
            file.seek(0)
        
            # Set file overwrite to true
            overwrite = "Y"

            # Make list of all inputs
            input_list = [
                file_name,
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

                try:

                    # Run PLC with parameters
                    PLC()

                finally:

                    # Reset output to standard output
                    io_stream.reset_output()

                    # Close the file
                    file.close()

                    # Delete file after using it
                    remove(file_name)

                # Open output file
                with open(outfile_name) as file:

                    # Read and return lines from output file
                    return [line.strip() for line in file.readlines() if line.strip() != ""]
    
    def test_python_1(self):
        """Test Case for file - test_exampes/python_1.py"""

        # Set input parameters
        lang_to = "java"
        outfile_name = "test_examples/python_1_outfile.java"

        # Create list to store file content
        file_content = [
            "def main():",
            "    print(\"Hello World\")"
            "",
            "",
            "if __name__ == \"__main__\":",
            "    main()"
        ]

        # Set expected ouput
        expected_output = [line.strip() for line in """
        class Python_1_Outfile {
            public static void main(String[] args) {
                System.out.println("Hello World\\n");
            }
        }""".split("\n") if line.strip() != ""]

        # Get PLC ouput
        PLC_output = self.get_output(
            file_content,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual([line.strip() for line in PLC_output],
                          expected_output)

    def test_python_2(self):
        """Test Case for file - test_exampes/python_2.py"""

        # Set input parameters
        lang_to = "java"
        outfile_name = "test_examples/python_2_outfile.java"

        # Create list to store file content
        file_content = [
            "def main():",
            "    value = 1",
            "    if value == 0:",
            "        print(\"False\")",
            "    elif value == 1:",
            "        print(\"True\")",
            "    else:",
            "        print(\"Undefined\")",
        ]

        # Set expected ouput
        expected_output = [line.strip() for line in """
        class Python_2_Outfile {
            public static void main(String[] args) {
                int value = 1;
                if (value == 0) {
                    System.out.println("False\\n");
                }
                else if (value == 1) {
                    System.out.println("True\\n");
                }
                else {
                   System.out.println("Undefined\\n");
                }
            }
        }""".split("\n") if line.strip() != ""]

        # Get PLC ouput
        PLC_output = self.get_output(
            file_content,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual(expected_output,
                         [line.strip() for line in PLC_output])

    def test_python_3(self):
        """Test Case for file - test_exampes/python_3.py"""

        # Set input parameters
        lang_to = "java"
        outfile_name = "test_examples/python_3_outfile.java"

        # Create list to store file content
        file_content = [
            "def main():",
            "    j = 0",
            "    for i in range(10):",
            "        j += i",
            "        print(str(i) + str(j))"
        ]

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
            file_content,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual(expected_output,
                         [line.strip() for line in PLC_output])


    def test_python_4(self):
        """Test Case for file - test_exampes/python_4.py"""

        # Set input parameters
        lang_to = "java"
        outfile_name = "test_examples/python_4_outfile.java"

        # Create list to store file content
        file_content = [
            "def main():",
            "    print(\"Ends with '!'\", end=\"!\")"
        ]

        # Set expected ouput
        expected_output = [line.strip() for line in """
        class Python_4_Outfile {
            public static void main(String[] args) {
                System.out.println("Ends with '!'!");
            }
        }""".split("\n") if line.strip() != ""]

        # Get PLC ouput
        PLC_output = self.get_output(
            file_content,
            lang_to,
            outfile_name)

        # Compare ouput with expected ouput
        self.assertEqual(expected_output,
                         [line.strip() for line in PLC_output])


if __name__ == "__main__":
    unittest.main()
