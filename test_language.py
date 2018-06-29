import unittest
from language import Language
from os import path


class TestLanguage(unittest.TestCase):
    def test_get_language(self):
        """Tests Language.get_language"""
        
        # Create test set with valid data
        valid_test_set = [
            (".py", "python"),
            (".java", "java"),
            (".cpp", "cpp"),
            (".c", "c"),
            (u".java", "java"),
            (".JaVa", "java"),
            (".JAVA", "java"),
        ]

        # Create test set with invalid data
        unsupported_error = "Unsupported file extension {}"
        invalid_type_error = "Parameter extension must be a string"
        
        # Create test set with unsupported extensions
        unsupported_test_set = [
            ".rand",
            "blah",
            ".1234",
            "\x03",
        ]

        # Create test set with invalid types
        invalid_type_test_set = [
            1234,
            b".py",
        ]

        # Add expected response
        for i, test in enumerate(unsupported_test_set):
            unsupported_test_set[i] = (test, (None, unsupported_error.format(test)))

        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] = (test, (None, invalid_type_error))

        # Merge invalid test sets
        invalid_test_set = unsupported_test_set + invalid_type_test_set

        # Merge both test sets
        test_set = valid_test_set + invalid_test_set

        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(Language.get_language(test[0]), test[1])
    
    def test_recognize(self):
        """Tests Language.recognize"""

        # Create test set with valid data
        valid_test_set = [
            "python_file.py",
            "java_file.java",
            "cpp_file.cpp",
            "c_file.c",
            "java_file.JAVA",
            "java_file.JaVa",
            "python_\x09.py",
        ]

        # Add expected response
        for i, test in enumerate(valid_test_set):
            valid_test_set[i] = (test, test.split('_')[0].lower())

        # Create test set with invalid date
        unsupported_error = "Unsupported file extension {}"
        invalid_type_error = "Parameter file_path must be a string"
        
        # Create test set for unsupported languages
        unsupported_test_set = [
            "Unsupported_file_type.abc",
            "Unsupported_random_file_type.random",
            "Unsupported_num_file.123",
            "\x03.hex",
        ]

        # Create test set for invalid types
        invalid_type_test_set = [
            1234,
            b'python_file.py',
        ]

        # Add expected results
        for i, test in enumerate(unsupported_test_set):
            unsupported_test_set[i] = (
                test,
                (None, unsupported_error.format(path.splitext(test)[1]))
            )
        
        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] = (test, (None, invalid_type_error))

        # Merge invalid test sets
        invalid_test_set = unsupported_test_set + invalid_type_test_set
        
        # Merge both test sets
        test_set = valid_test_set + invalid_test_set

        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(Language.recognize(test[0]), test[1])

    def test_validate(self):
        """Tests Language.validate"""
        
        # Create test set with valid data
        valid_test_set = [
            "python",
            "java",
            "cpp",
            "c",
            u"java",
            "JAVA",
        ]

        # Add expected response
        valid_return_value = None
        for i, test in enumerate(valid_test_set):
            valid_test_set[i] = (test, valid_return_value)

        # Create test set with invalid data
        unsupported_error = "Unsupported language {}"
        invalid_type_error = "Parameter language must be a string"
        
        # Create test set with unsupported languages
        unsupported_test_set = [
            "rand",
            "blah",
            "1234",
            ".py",
            "python_",
            "\x03",
        ]

        # Create test set with invalid type
        invalid_type_test_set = [
            1234,
            b"java",
        ]

        # Add expected results
        for i, test in enumerate(unsupported_test_set):
            unsupported_test_set[i] = (test, unsupported_error.format(test))

        for i, test in enumerate(invalid_type_test_set):
            invalid_type_test_set[i] = (test, invalid_type_error.format(test))

        # Merge invalid test sets
        invalid_test_set = unsupported_test_set + invalid_type_test_set

        # Merge valid test sets
        test_set = valid_test_set + invalid_test_set

        # Run test for all tests in test_set
        for test in test_set:
            self.assertEqual(Language.validate(test[0]), test[1])

    def test_convert_if(self):
        """Test case for Language.convert_if"""

        # Create test set
        test_set = [
            "cond1 && cond2 || cond3 && !(!cond4)"
        ]
        
        # Create expected results test set
        res_set = [
            "cond1 && cond2 || cond3 && !(!cond4)"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().convert_if(test_set[i]), res_set[i]
            )
        
    def test_convert_for(self):
        """Test case for Language.convert_for"""

        # Create test set
        test_set = [
            ("i", "0", "10", "1", None),
            ("arr_item", "0", "10", "1", "arr")
        ]
        
        # Create expected results test set
        res_set = [
            ("i", "0", "10", "1", None),
            ("arr_item", "0", "10", "1", "arr")
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().convert_for(*test_set[i]), res_set[i]
            )
        
    def test_convert_while(self):
        """Test case for Language.convert_while"""

        # Create test set
        test_set = [
            "cond1 || cond2 && are_met"
        ]
        
        # Create expected results test set
        res_set = [
            "cond1 || cond2 && are_met"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().convert_while(test_set[i]), res_set[i]
            )
        
    def test_convert_function(self):
        """Test case for Language.convert_function"""

        # Create test set
        test_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count", [])
        ]
        
        # Create expected results test set
        res_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count", [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().convert_function(*test_set[i]), res_set[i]
            )
        
    def test_convert_method(self):
        """Test case for Language.convert_method"""

        # Create test set
        test_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count", [])
        ]
        
        # Create expected results test set
        res_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count", [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().convert_method(*test_set[i]), res_set[i]
            )
        
    def test_convert_class(self):
        """Test case for Language.convert_class"""

        # Create test set
        test_set = [
            ("public", "ChildClass", ["ParentClass"], ["MyInterface"]),
            ("", "MyClass", [], [])
        ]
        
        # Create expected results test set
        res_set = [
            ("public", "ChildClass", ["ParentClass"], ["MyInterface"]),
            ("", "MyClass", [], [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().convert_class(*test_set[i]), res_set[i]
            )
        
    def test_convert_interface(self):
        """Test case for Language.convert_interface"""

        # Create test set
        test_set = [
            ("public", "ChildIntr", ["ParentIntr", "SuperIntr"]),
            ("", "MyIntr", [])
        ]
        
        # Create expected results test set
        res_set = [
            ("public", "ChildIntr", ["ParentIntr", "SuperIntr"]),
            ("", "MyIntr", [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().convert_interface(*test_set[i]), res_set[i]
            )
        
    def test_get_if_condition(self):
        """Test case for Language.get_if_condition"""

        # Create test set
        test_set = [
            (["if name and uid:"], 0),
            (["if (name && uid) {"], 0)
        ]
        
        # Create expected results test set
        res_set = [
            "name and uid:",
            "(name && uid)"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().get_if_condition(*test_set[i]), res_set[i]
            )
        
    def test_get_for_iterations(self):
        """Test case for Language.get_for_iterations"""

        # Create test set
        test_set = [
            (["for i in range(10):"], 0),
            (["for (int i=0; i<10; i++) {"], 0)
        ]
        
        # Create expected results test set
        res_set = [
            ["i", "in", "range(10"],
            ["int i=0", "i<10", "i++"]
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().get_for_iterations(*test_set[i]), res_set[i]
            )
        
    def test_get_while_condition(self):
        """Test case for Language.get_while_condition"""

        # Create test set
        test_set = [
            (["while (cond1 || cond2 && are_met) {"], 0),
            (["while cond1 or cond2 and are_met:"], 0)
        ]
        
        # Create expected results test set
        res_set = [
            "(cond1 || cond2 && are_met)",
            "cond1 or cond2 and are_met:"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().get_while_condition(*test_set[i]), res_set[i]
            )
        
    def test_get_function_definition(self):
        """Test case for Language.get_function_definition"""

        # Create test set
        test_set = [
            (["public static void main(String[] args) {"], 0),
            (["def main():"], 0)
        ]
        
        # Create expected results test set
        res_set = [
            ("public static void main", "String[] args)"),
            ("def main", "):")
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().get_function_definition(*test_set[i]), res_set[i]
            )
        
    def test_get_method_definition(self):
        """Test case for Language.get_method_definition"""

        # Create test set
        test_set = [
            (["public static void main(String[] args) {"], 0),
            (["def main():"], 0)
        ]
        
        # Create expected results test set
        res_set = [
            ("public static void main", "String[] args)"),
            ("def main", "):")
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().get_method_definition(*test_set[i]), res_set[i]
            )

    def test_get_class_definition(self):
        """Test case for Language.get_class_definition"""

        # Create test set
        test_set = [
            (["public class MyClass extends ParentClass implement MyIntr"], 0),
            (["class MyClass(ParentClass, MyIntr):"], 0)
        ]
        
        # Create expected results test set
        res_set = [
            "public class MyClass extends ParentClass implement MyIntr",
            "MyClass(ParentClass, MyIntr):"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().get_class_definition(*test_set[i]), res_set[i]
            )
        
    def test_get_interface_definition(self):
        """Test case for Language.get_interface_definition"""

        # Create test set
        test_set = [
            (["interface ParentIntr"], 0),
            (["public static interface MyIntr extends ParentIntr"], 0)
        ]
        
        # Create expected results test set
        res_set = [
            "ParentIntr",
            "public static interface MyIntr extends ParentIntr"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().get_interface_definition(*test_set[i]), res_set[i]
            )
        
    def test_is_if(self):
        """Test case for Language.is_if"""

        # Create test set
        test_set = [
            ([], 0)
        ]
        
        # Create expected results test set
        res_set = [
            None
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().is_if(*test_set[i]), res_set[i]
            )
        
    def test_is_for(self):
        """Test case for Language.is_for"""

        # Create test set
        test_set = [
            ([], 0)
        ]
        
        # Create expected results test set
        res_set = [
            None
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().is_for(*test_set[i]), res_set[i]
            )
        
    def test_is_while(self):
        """Test case for Language.is_while"""

        # Create test set
        test_set = [
            ([], 0)
        ]
        
        # Create expected results test set
        res_set = [
            None
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().is_while(*test_set[i]), res_set[i]
            )
        
    def test_is_func(self):
        """Test case for Language.is_func"""

        # Create test set
        test_set = [
            ([], 0)
        ]
        
        # Create expected results test set
        res_set = [
            None
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().is_func(*test_set[i]), res_set[i]
            )
        
    def test_is_method(self):
        """Test case for Language.is_method"""

        # Create test set
        test_set = [
            ([], 0)
        ]
        
        # Create expected results test set
        res_set = [
            None
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().is_method(*test_set[i]), res_set[i]
            )
        
    def test_is_cls(self):
        """Test case for Language.is_cls"""

        # Create test set
        test_set = [
            ([], 0)
        ]
        
        # Create expected results test set
        res_set = [
            None
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().is_cls(*test_set[i]), res_set[i]
            )
        
    def test_is_interface(self):
        """Test case for Language.is_interface"""

        # Create test set
        test_set = [
            ([], 0)
        ]
        
        # Create expected results test set
        res_set = [
            None
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Language().is_interface(*test_set[i]), res_set[i]
            )
        

if __name__ == '__main__':
    unittest.main()
