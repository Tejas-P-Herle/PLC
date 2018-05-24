"""Tests languages.python.Python"""
import unittest
from languages.python import Python


class TestPython(unittest.TestCase):
    file = """
class ParentCls:
    def __init__(self):
        print("Initiating Class: ParentCls")


class ChildCls(ParentCls):
    occupied = False
    processes_running = 100

    def my_func(self, name):
        if not occupied and not(processes_running > 500):
            if (name != "" and name) or default:
                print("Name: ", name)

    def for_func(self, count):
        for i in range(count):
            print(i)
        for i in range(5, count):
            print(i)
        for i in range(0, count, 2):
            print(i)

class MyIntr:
    '''class type: interface'''
    pass

class ChildIntr(MyIntr):
    '''class type: interface
    MyIntr: interface'''
    pass

@my_dec
@staticmethod
def main():
    running = True
    i = -
    while running:
        c = ChildCls()
        c.my_func("Tejas")
        i += 1
        if i == 10:
            running = False

if __name__ == "__main__":
    main()
""".split("\n")

    def test_replace_logical_ops(self):
        """Tests Python.test_replace_logical_ops"""

        # Create test set for function
        test_set = [
            "and_str and or_str or not_str and not and_or_not_str",
            "name and uid or reg_no and not unknown and not(std < 1)",
            "&&_str and ||_str or n!_str and u! &&_||_!_str"
        ]

        # Create expected results test set for function
        res_set = [
            "and_str && or_str || not_str && !and_or_not_str",
            "name && uid || reg_no && !unknown && !(std < 1)",
            "&&_str && ||_str || n!_str && u! &&_||_!_str"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test from conversion
            self.assertEqual(Python().replace_logical_ops(test_set[i], "to"),
                             res_set[i])

            # Test to conversion
            self.assertEqual(Python().replace_logical_ops(res_set[i], "from"),
                             test_set[i])

    def test_get_list_slice_vars(self):
        """Tests Python.get_list_slice_vars"""

        # Create test set for function
        test_set = [
            "array[:10]",
            "my_array[4:]",
            "dual_in_arr[2:10]",
            "step_arr[0:10:5]"
        ]

        # Create expected results test set for function
        res_set = [
            ("array", "0", "10", "1"),
            ("my_array", "4", "Array.length", "1"),
            ("dual_in_arr", "2", "10", "1"),
            ("step_arr", "0", "10", "5")
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().get_list_slice_vars(test_set[i]),
                             res_set[i])

    def test_get_type(self):
        """Tests Python.get_type"""

        # Create test set for function
        test_set = [
            "0",
            "213.456",
            "23j",
            "'string'",
            '"Double quote string"',
            "[0, 1, 2, 3]",
            "('This', 'is', 'a', 'tuple')",
            "{'key': 'value'}"
        ]

        # Create expected results test set for function
        res_set = [
            "int",
            "float",
            "complex",
            "str",
            "str",
            "list",
            "tuple",
            "dict"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().get_type(test_set[i]),
                             res_set[i])

    def test_parse_function_definition(self):
        """Tests Python.parse_function_definition"""

        # Create test set for function
        test_set = [
            (self.file, 34, "def main", "):"),
            (self.file, -1, "def func_name", "var: 'int') -> 'int':")
        ]

        # Create expected results test set for function
        res_set = [
           ("void", "main", [], ["staticmethod", "main = my_dec(main)"]),
           ("int", "func_name", [["var", 'int']], []) 
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().parse_function_definition(*test_set[i]),
                             res_set[i])

    def test_make_function_definition(self):
        """Tests Python.make_function_definition"""

        # Create test set for function
        test_set = [
            ("void", "main", []),
            ("int", "func_name", [["var", 'int']])
        ]

        # Create expected results test set for function
        res_set = [
            "def main() -> 'None':",
            "def func_name(var: 'int') -> 'int':"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().make_function_definition(*test_set[i]),
                             res_set[i])

    def test_get_class_name(self):
        """Tests Python.get_class_name"""

        # Create test set for function
        test_set = [
            (self.file, 10),
            (self.file, 30),
            (self.file, 25)
        ]

        # Create expected results test set for function
        res_set = [
           "ChildCls",
           "ChildIntr",
           "MyIntr"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().get_class_name(*test_set[i]),
                             res_set[i])

    def test_get_doc_str(self):
        """Tests Python.get_doc_str"""

        # Create test set for function
        test_set = [
            (self.file, 23),
            (self.file, 27)
        ]

        # Create expected results test set for function
        res_set = [
            ["class type: interface"],
            ["class type: interface", "MyIntr: interface"]
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().get_doc_str(*test_set[i]),
                             res_set[i])

    def test_convert_if(self):
        """Tests Python.convert_if"""

        # Create test set for function
        test_set = [
            "name && uid || reg_no && !unknown && !(std < 1)",
            "_!name && ||uid || |||| && &&&&&&&",
            "!!",
            "!(!)"
        ]

        # Create expected results test set for function
        res_set = [
           "if name and uid or reg_no and not unknown and not(std < 1):",
           "if _!name and ||uid or |||| and &&&&&&&:",
           "if not !:",
           "if not(not):"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().convert_if(test_set[i]),
                             [res_set[i]])

    def test_convert_for(self):
        """Tests Python.convert_for"""

        # Create test set for function
        test_set = [
            ("i", "0", "10", "1", None),
            ("i", "2", "10", "1", None),
            ("i", "0", "10", "2", None),
            ("i", "0", "Array.length", "1", "array"),
            ("i", "2", "Array.length", "2", "array"),
        ]

        # Create expected results test set for function
        res_set = [
           "for i in range(10):",
           "for i in range(2, 10):",
           "for i in range(0, 10, 2):",
           "for i in array:",
           "for i in array[2::2]:"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().convert_for(*test_set[i]),
                             [res_set[i]])

    def test_convert_while(self):
        """Tests Python.convert_while"""

        # Create test set for function
        test_set = [
            "count < 100 && !(count == 0 || count < 0) && !error",
            "!user_input.valid() && !(user_input.quit || one_shot)"
        ]

        # Create expected results test set for function
        res_set = [
            "while count < 100 and not(count == 0 or count < 0) and not error:",
            "while not user_input.valid() and not(user_input.quit or one_shot):"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().convert_while(test_set[i]),
                             [res_set[i]])

    def test_convert_function(self):
        """Tests Python.convert_function"""

        # Create test set for function
        test_set = [
            ("public static", "void", "main", []),
            ("", "int", "my_func", [["var", "String"]])
        ]

        # Create expected results test set for function
        res_set = [
           "def main() -> 'None':",
           "def my_func(var: 'String') -> 'int':"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().convert_function(*test_set[i]),
                             [res_set[i]])

    def test_convert_method(self):
        """Tests Python.convert_method"""

        # Create test set for function
        test_set = [
            ("public static", "void", "main", []),
            ("public", "String", "my_func", [["var", "float"]])
        ]

        # Create expected results test set for function
        res_set = [
           ["@staticmethod", "def main() -> 'None':"],
           ["def my_func(var: 'float') -> 'String':"]
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test function with inputs and expected outputs
            self.assertEqual(Python().convert_method(*test_set[i]),
                             res_set[i])

    def test_convert_class(self):
        """Tests Python.convert_class"""

        # Create test set for class
        test_set = [
            ("public", "ClassName", ["ParentClass"], ["SuperIntr", "MyIntr"]),
            ("public", "MyClass", ["SuperClass"], ["RandIntr"]),
            ("public", "RandClass", ["MyClass"], []),
            ("public", "MyOwnClass", [], ["MyOwnIntr"]),
            ("public", "BareClass", [], [])
        ]

        # Create expected results test set for class
        res_set = [
            ["class ClassName(ParentClass, SuperIntr, MyIntr):",
             '"""SuperIntr: interface',
             'MyIntr: interface"""'],
            ["class MyClass(SuperClass, RandIntr):",
             '"""RandIntr: interface"""'],
            ["class RandClass(MyClass):"],
            ["class MyOwnClass(MyOwnIntr):",
             '"""MyOwnIntr: interface"""'],
            ["class BareClass:"]
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test class with inputs and expected outputs
            self.assertEqual(Python().convert_class(*test_set[i]),
                             res_set[i])

    def test_convert_interface(self):
        """Tests Python.convert_interface"""

        # Create test set for interface
        test_set = [
            ("IntrName", ["ParentIntr", "SuperIntr"]),
            ("RandIntr", ["MyIntr"]),
            ("Interface", []),
        ]

        # Create expected results test set for interface
        res_set = [
            ["class IntrName(ParentIntr, SuperIntr):",
             '"""class type: interface',
             "ParentIntr: interface", 
             'SuperIntr: interface"""'],
            ["class RandIntr(MyIntr):",
             '"""class type: interface',
             'MyIntr: interface"""'],
            ["class Interface:",
             '"""class type: interface"""']
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test interface with inputs and expected outputs
            self.assertEqual(Python().convert_interface(*test_set[i]),
                             res_set[i]) 
    def test_convert_decorator(self):
        """Tests Python.convert_decorator"""

        # Create test set for decorator
        test_set = [
            ("@my_dec", "my_func"),
            ("@staticmethod", "my_static_func")
        ]

        # Create expected results test set for decorator
        res_set = [
            "my_func = my_dec(my_func)",
            "my_static_func = staticmethod(my_static_func)"
        ]
 
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Test decorator with inputs and expected outputs
            self.assertEqual(Python().convert_decorator(*test_set[i]),
                             [res_set[i]])


if __name__ == "__main__":
    unittest.main()
