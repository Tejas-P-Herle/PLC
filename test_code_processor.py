import unittest
from tempfile import TemporaryFile
import os
import re

from code_processor import CodeProcessor
from language import Language
from languages.python import Python
from languages.java import Java
from languages.c import C
from languages.cpp import CPP
from logger import Logger


class TestCodeProcessor(unittest.TestCase):
    def test___init__(self):
        """Test case for CodeProcessor.__init__"""

        # Create test set
        test_set = [
            ("test_examples/python_1.py", "python", "java", "test_examples/java.py")
        ]

        # Create language class dictionary
        lang_cls_dict = {
            "python": Python,
            "java": Java,
            "c": C,
            "cpp": CPP,
        }

        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Create class instance
            processor = CodeProcessor(*test_set[i])

            # Create from language class
            lang_cls = lang_cls_dict[test_set[i][1].lower()]()

            # Create duplicate of language functions
            funcs = [func.__code__.co_code for func in [
                lang_cls.convert_if, lang_cls.convert_for, lang_cls.convert_while,
                lang_cls.convert_function, lang_cls.convert_method,
                lang_cls.convert_class, lang_cls.convert_interface,
                lang_cls.get_if_condition, lang_cls.get_for_iterations,
                lang_cls.get_while_condition, lang_cls.get_function_definition,
                lang_cls.get_method_definition, lang_cls.get_class_definition,
                lang_cls.get_interface_definition, lang_cls.is_if, lang_cls.is_for,
                lang_cls.is_while, lang_cls.is_func, lang_cls.is_method,
                lang_cls.is_cls, lang_cls.is_interface,
            ]]

            # Create duplicate of recognition functions
            rec = [
                lang_cls.is_if, lang_cls.is_for, lang_cls.is_while,
                lang_cls.is_func, lang_cls.is_method, lang_cls.is_cls,
                lang_cls.is_interface,
            ]

            rec_funcs = [func.__code__.co_code for func in rec]
            rec_names = [func.__name__ for func in rec]

            # Create set of from_conversion functions
            from_conv_funcs = [func.__code__.co_code for func in [
                lang_cls.get_if_condition, lang_cls.get_for_iterations,
                lang_cls.get_while_condition, lang_cls.get_function_definition,
                lang_cls.get_method_definition, lang_cls.get_class_definition,
                lang_cls.get_interface_definition,
            ]]

            # Create to language class
            lang_cls = lang_cls_dict[test_set[i][2].lower()]()

            # Create set of to_convertion_functions
            to_conv_funcs = [func.__code__.co_code for func in [
                lang_cls.convert_if, lang_cls.convert_for, lang_cls.convert_while,
                lang_cls.convert_function, lang_cls.convert_method,
                lang_cls.convert_class, lang_cls.convert_interface,
            ]]

            # Create functions map
            funcs_map = {
                rec_names[0]: (from_conv_funcs[0], to_conv_funcs[0]),
                rec_names[1]: (from_conv_funcs[1], to_conv_funcs[1]),
                rec_names[2]: (from_conv_funcs[2], to_conv_funcs[2]),
                rec_names[3]: (from_conv_funcs[3], to_conv_funcs[3]),
                rec_names[4]: (from_conv_funcs[4], to_conv_funcs[4]),
                rec_names[5]: (from_conv_funcs[5], to_conv_funcs[5]),
                rec_names[6]: (from_conv_funcs[6], to_conv_funcs[6]),
            }
        
            # Set language indentation preferance
            indent_preference = 2

            # Check to langauge
            if test_set[i][2] == "python":
                
                # Then change indent_preferance to 4
                indent_preference = 4

            # Create expected results test set
            res_set = [*test_set[i]]\
                + [0, 0, 0, 0, 0,
                   True, True, indent_preference, [], []
                   ]

            # Create data set of derived values
            data_set = [
                processor.file_path, processor.lang_from,
                processor.lang_to, processor.outfile_path,
                len(['' for func in processor.funcs
                     if func.__code__.co_code not in funcs]),
                len(['' for func in processor.rec_funcs
                     if func.__code__.co_code not in rec_funcs]),
                len(['' for func in processor.from_conv_funcs
                     if func.__code__.co_code not in from_conv_funcs]),
                len(['' for func in processor.to_conv_funcs
                     if func.__code__.co_code not in to_conv_funcs]),
                len(['' for rec, func in processor.funcs_map.items()
                     if (func[0].__code__.co_code,
                         func[1].__code__.co_code,
                         ) not in funcs_map.values() or 
                     rec not in funcs_map.keys()]),
                isinstance(processor.from_cls, Language),
                isinstance(processor.to_cls, Language),
                processor.to_indent_preference,
                processor.vars, processor.file_lines,
            ]
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                data_set, res_set
            )
        
    def test_indent(self):
        """Test case for CodeProcessor.indent"""

        # Create test set
        test_set = ["    4 Indent line",
                    "    Tab indent line",
                    "        8 Indent line",
                    "        Mix Indent line",
                    "        Mix 2 Indent line",
                    "  2 Indent line",
                    "          10 mix indent line",
                    "      6 Indent line"]
        
        # Create expected results test set
        res_set = [4, 4, 8, 8, 8, 2, 10, 6]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").indent(test_set[i]), res_set[i]
            )
        
    def test_convert(self):
        """Test case for CodeProcessor.convert"""
        
        # Create temporary file names
        test_set = [
            ["def main():",
             "    print(\"Hello World\")",
             "",
             "",
             "if __name__ == \"__main__\":",
             "    main()"],
            ["def main():",
             "    print(\"Hello World 2\", end=\"\")",
             "",
             "",
             "if __name__ == \"__main__\":",
             "    main()"],
        ]

        # Create expected results test set
        res_set = [
            ["class Temp_Outfile {",
             "  public static void main(String[] args) {",
             "    System.out.println(\"Hello World\\n\");",
             "  }",
             "}", "", ""],
            ["class Temp_Outfile {",
             "  public static void main(String[] args) {",
             "    System.out.println(\"Hello World 2\");",
             "  }",
             "}", "", ""],
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Make new temporary file
            with TemporaryFile(suffix=".py", dir=".", mode="x+") as file:
                
                # Write test program to file
                file.write("\n".join(test_set[i]))

                # Save file name
                file_name = file.name

                # Seek start of file
                file.seek(0)

                try:
                    # Create Code Processor instance
                    processor = CodeProcessor(file_name, "python", "java",
                                              "temp_outfile.java")

                    # Convert file
                    processor.convert()

                finally:

                    # Close the file
                    file.close()

                    # Delete file after using it
                    os.remove(file_name)

                # Test function with inputs and expected outputs
                self.assertEqual(processor.file_lines, res_set[i])

    def test_regex_substitute(self):
        """Test case for CodeProcessor.regex_substitute"""

        # Create test set suppliment list
        test_set_suppliment = [
            (r"print\(([$1][\"'][^\"']*)([$2][\"'])\)",
             "    print('Hello World')",
             r"System.out.println\(([$1][\"'][^\\]*)\\n([$2][\"'])\)",
             "    System.out.println('Hello World\\n')"),
            (r"print\(([$1]([\"'])[^\"']*)([$2]\2), end=([$3][\"'])([$3][\"'])\)",
             "    print('Hello World', end=\"\")",
             r"System\.out\.println\(([$1]([\"'])[^\"']*)([$2]\2)\)",
             "    System.out.println('Hello World')"),
            (r"print\(([$1][\"'].*)([$3][\"']), end=([$3][\"'])([$2][^,]+?)([$3][\"'])\)",
             "    print('Hello World', end=\"\\n\")",
             r"System\.out\.println\(([$1][\"'][^\\)]*)([$4]\\[a-z])([$2][\"'])\)",
             "    System.out.println('Hello World\\n')"),
            (r"(?<!int {1})([$1]\S+ [+\-*/]{0,2}= [0-9]+)",
             "    var_num = 10",
             r"int ([$1]\S+[\s\t]*[+\-*/]{0,2}=[\s\t]*[0-9]+)",
             "    int var_num = 10")
        ]

        # Create empty test set list
        test_set = []

        # Iterate over data in test set suppliment list
        for data in test_set_suppliment:
            
            # Add required data to test_set (from conversion)
            match_str = re.sub(r"\[\$[0-9]\]", "", data[0])
            test_set.append(
                (data[0], match_str, re.match(match_str, data[1].strip()),
                 data[2], data[1]))
            
            # Add required data to test_set (to conversion)
            match_str = re.sub(r"\[\$[0-9]\]", "", data[2])
            test_set.append(
                (data[2], match_str, re.match(match_str, data[3].strip()),
                 data[0], data[3]))


        # Create expected results test set
        res_set = ["    System.out.println('Hello World\\n')",
                   "    print('Hello World')",
                   "    System.out.println('Hello World')",
                   "    print('Hello World', end='')",
                   "    System.out.println('Hello World\\n')",
                   "    print('Hello World', end='\\n')",
                   "    int var_num = 10",
                   "    var_num = 10"]
        
        # Run test for all tests in test_set
        for i in range(0, len(test_set), 2):
        
            # Test function with inputs and expected outputs (from conversion)
            self.assertEqual(
                 CodeProcessor("test_examples/python_1.py", "python", "java",
                               "outfile.java").regex_substitute(*test_set[i]),
                                res_set[i])

            # Test function with inputs and expected outputs (to conversion)
            self.assertEqual(
                 CodeProcessor("test_examples/java_1.java", "java", "python",
                               "outfile.py").regex_substitute(*test_set[i+1]),
                                res_set[i+1])
        
    def test_replace_group_no(self):
        """Test case for CodeProcessor.replace_group_no"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").replace_group_no(*test_set[i]),
                                res_set[i])
        
    def test_write_to_file(self):
        """Test case for CodeProcessor.write_to_file"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").write_to_file(*test_set[i]),
                                res_set[i])
        
    def test_add_endings(self):
        """Test case for CodeProcessor.add_endings"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").add_endings(*test_set[i]), res_set[i]
            )
        
    def test_is_def_end(self):
        """Test case for CodeProcessor.is_def_end"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").is_def_end(*test_set[i]),
                               res_set[i])
        
    def test_get_indent_base(self):
        """Test case for CodeProcessor.get_indent_base"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").get_indent_base(*test_set[i]),
                               res_set[i])
        
    def test_recognize(self):
        """Test case for CodeProcessor.recognize"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").recognize(*test_set[i]),
                                res_set[i])
        
    def test_match_regex(self):
        """Test case for CodeProcessor.match_regex"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").match_regex(),
                               res_set[i])
        
    def test_read_conv_db(self):
        """Test case for CodeProcessor.read_conv_db"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").read_conv_db(),
                               res_set[i])
        
    def test_write_file_to_disk(self):
        """Test case for CodeProcessor.write_file_to_disk"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java",
                               "outfile.java").write_file_to_disk(),
                               res_set[i])
        

if __name__ == '__main__':
    unittest.main()
