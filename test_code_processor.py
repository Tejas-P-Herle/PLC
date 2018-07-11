import unittest
from code_processor import CodeProcessor


class TestCodeProcessor(unittest.TestCase):
    def test___init__(self):
        """Test case for CodeProcessor.__init__"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").__init__(*test_set[i]), res_set[i]
            )
        
    def test_indent(self):
        """Test case for CodeProcessor.indent"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").indent(*test_set[i]), res_set[i]
            )
        
    def test_convert(self):
        """Test case for CodeProcessor.convert"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").convert(*test_set[i]), res_set[i]
            )
        
    def test_regex_substitute(self):
        """Test case for CodeProcessor.regex_substitute"""

        # Create test set
        test_set = []
        
        # Create expected results test set
        res_set = []
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").regex_substitute(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").replace_group_no(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").write_to_file(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").add_endings(*test_set[i]), res_set[i]
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").is_def_end(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").get_indent_base(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").recognize(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").match_regex(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").read_conv_db(*test_set[i]), res_set[i]
            )
        
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
                 CodeProcessor("test_cases/python_file_1.py", "python", "java", "outfile.java").write_file_to_disk(*test_set[i]), res_set[i]
            )
        

if __name__ == '__main__':
    unittest.main()