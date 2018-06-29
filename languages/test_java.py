import unittest
from languages.java import Java


class TestJava(unittest.TestCase):
    file = """
private static class ParentClass {}

public static interface ParentIntr {}

private interface MyIntr extends ParentIntr {}

class ExtClass extends ParentClass implements ParentIntr, MyIntr {
    private bool accept_null = False;
    public static int run_ext_func(int times) {
        if (times < 0 && !accept_null) {
            System.out.println("ERROR: 'times' less than 0)
        }

        if (times == 10)
            this.print_default_times()

        for (int i=0; i<times; i++)
            System.out.println("Running ext_func");
        return 0;

     void print_default_times() {
        for( int i=0; i<10; i+=2)
            System.out.println("Running ext_func");
     }

public class MyProgram {
    public static void main(String[] args) {
        for (int i = 2; i< 10; i++)
            System.out.printf("%d", i);
        for (int j=0; j >= -10; j -= 2)
            System.out.printf("%d", j);
        bool valid = True;
        while (valid) {
            System.out.println("isValid = True");
            valid = False;
        }
        int[] my_arr = {1, 2, 3, 4, 5};
        for (int num: my_arr)
            System.out.println(num);
        run_ext_func();
    }

}
""".split("\n")

    def test_parse_function_definition(self):
        """Test case for Java.parse_function_definition"""

        # Create test set
        test_set = [
            ("public static void main", "String[] args) {"),
            ("int count_occurrences", "File fp) {"),
            ("private String[] my_func", ") {")
        ]
        
        # Create expected results test set
        res_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count_occurrences", [["fp", "File"]]),
            ("private", "String[]", "my_func", [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().parse_function_definition(*test_set[i]), res_set[i]
            )
        
    def test_make_function_definition(self):
        """Test case for Java.make_function_definition"""

        # Create test set
        test_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count_occurrences", [["fp", "File"]]),
            ("private", "String[]", "my_func", [])
        ]
        
        # Create expected results test set
        res_set = [
            "public static void main(String[] args) {",
            "int count_occurrences(File fp) {",
            "private String[] my_func() {",
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().make_function_definition(*test_set[i]), res_set[i]
            )
        
    def test_convert_if(self):
        """Test case for Java.convert_if"""

        # Create test set
        test_set = [
            "name && uid || reg_no && !invalid && !(time > expired)",
            "&&_text && ||_text || u!_text && &&&&&&&&&||&& || |||!||"
        ]
        
        # Create expected results test set
        res_set = [
            "if (name && uid || reg_no && !invalid && !(time > expired)) {",
            "if (&&_text && ||_text || u!_text && &&&&&&&&&||&& || |||!||) {"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().convert_if(test_set[i]), ([res_set[i]], ["}"])
            )
        
    def test_convert_for(self):
        """Test case for Java.convert_for"""

        # Create test set
        test_set = [
            ("int i", "0", "10", "1", None),
            ("String var", "0", "10", "2", None),
            ("int var", "3", "30", "1", None),
            ("int j", "2", "20", "2", None),
            ("float arr_item", "0", "Array.length", "1", "my_array")
        ]
        
        # Create expected results test set
        res_set = [
            "for (int i = 0; i < 10; i++) {",
            "for (String var = 0; var < 10; var += 2) {",
            "for (int var = 3; var < 30; var++) {",
            "for (int j = 2; j < 20; j += 2) {",
            "for (float arr_item: my_array) {"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().convert_for(*test_set[i]), ([res_set[i]], ["}"]) 
            )
        
    def test_convert_while(self):
        """Test case for Java.convert_while"""

        # Create test set
        test_set = [
            "name && uid || reg_no && !invalid && !(time == expired)",
            "&&_text && ||_text || u!_text && &&&&&&&&&||&& || |||!||"
        ]
        
        # Create expected results test set
        res_set = [
            "while (name && uid || reg_no && !invalid && !(time == expired)) {",
            "while (&&_text && ||_text || u!_text && &&&&&&&&&||&& || |||!||) {"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().convert_while(test_set[i]), ([res_set[i]], ["}"]) 
            )
        
    def test_convert_function(self):
        """Test case for Java.convert_function"""

        # Create test set
        test_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count", [["file_name", "String"], ["kw", "String"]]),
            ("private", "void", "print_data", [])
        ]

        # Create expected results test set
        res_set = [
            ["class Outfile {",
             "    public static void main(String[] args) {"],
            ["int count(String file_name, String kw) {"],
            ["private void print_data() {"]
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            # Get number of closing brackets based on input
            end = ["}"] * (len(res_set[i]) if type(res_set[i]) == list else 1)

            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().convert_function(*test_set[i]), (res_set[i], end)
            )

    def test_convert_method(self):
        """Test case for Java.convert_method"""

        # Create test set
        test_set = [
            ("public static", "void", "main", [["args", "String[]"]]),
            ("", "int", "count", [["file_name", "String"], ["kw", "String"]]),
            ("private", "void", "print_data", [])
        ]
        
        # Create expected results test set
        res_set = [
            ["class Outfile {",
             "    public static void main(String[] args) {"],
            ["int count(String file_name, String kw) {"],
            ["private void print_data() {"]
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):

            # Get number of closing brackets based on input
            end = ["}"] * (len(res_set[i]) if type(res_set[i]) == list else 1)
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().convert_method(*test_set[i]), (res_set[i], end)
            )
        
    def test_convert_class(self):
        """Test case for Java.convert_class"""

        # Create test set
        test_set = [
            ("public final", "MasterClass", [], []),
            ("private static", "ChildClass", ["MasterClass"], ["ParentIntr"]),
            ("", "SubClass", ["MasterClass"], ["ParentIntr", "ChildIntr"]),
        ]
        
        # Create expected results test set
        res_set = [
            "public final class MasterClass {",
            "private static class ChildClass extends MasterClass"
            + " implements ParentIntr {",
            "class SubClass extends MasterClass"
            + " implements ParentIntr, ChildIntr {"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().convert_class(*test_set[i]), ([res_set[i]], ["}"]) 
            )

    def test_convert_interface(self):
        """Test case for Java.convert_interface"""

        # Create test set
        test_set = [
            ("public", "MyIntr", ["ParentIntr"]),
            ("private static", "ParentIntr", []),
            ("", "ChildIntr", ["MyIntr", "ParentIntr"])
        ]
        
        # Create expected results test set
        res_set = [
            "public interface MyIntr extends ParentIntr {",
            "private static interface ParentIntr {",
            "interface ChildIntr extends MyIntr, ParentIntr {"
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().convert_interface(*test_set[i]), ([res_set[i]], ["}"]) 
            )
        
    def test_get_if_condition(self):
        """Test case for Java.get_if_condition"""

        # Create test set
        test_set = [
            (self.file, 10),
            (self.file, 14)
        ]
        
        # Create expected results test set
        res_set = [
            ("times < 0 && !accept_null", [], []),
            ("times == 10", [], [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().get_if_condition(*test_set[i]), res_set[i]
            )
        
    def test_get_for_iterations(self):
        """Test case for Java.get_for_iterations"""

        # Create test set
        test_set = [
            (self.file, 17),
            (self.file, 22),
            (self.file, 28),
            (self.file, 30),
            (self.file, 38)
        ]
        
        # Create expected results test set
        res_set = [
            ("int i", "0", "times", "1", None, [], []),
            ("int i", "0", "10", "2", None, [], []),
            ("int i", "2", "10", "1", None, [], []),
            ("int j", "0", "-11", "-2", None, [], []),
            ("int num", "0", "Array.length", "1", "my_arr", [], [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().get_for_iterations(*test_set[i]), res_set[i]
            )
        
    def test_get_while_condition(self):
        """Test case for Java.get_while_condition"""

        # Create test set
        test_set = [
            (self.file, 33)
        ]
        
        # Create expected results test set
        res_set = [
            ("valid", [], [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().get_while_condition(*test_set[i]), res_set[i]
            )
        
    def test_get_function_definition(self):
        """Test case for Java.get_function_definition"""

        # Create test set
        test_set = [
            (self.file, 9),
            (self.file, 21),
            (self.file, 27)
        ]
        
        # Create expected results test set
        res_set = [
            ("public static", "int", "run_ext_func",
             [["times", "int"]], [], []),
            ("", "void", "print_default_times", [], [], []),
            ("public static", "void", "main", [["args", "String[]"]], [], []),
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().get_function_definition(*test_set[i]), res_set[i]
            )
        
    def test_get_method_definition(self):
        """Test case for Java.get_method_definition"""

        # Create test set
        test_set = [
            (self.file, 9),
            (self.file, 21),
            (self.file, 27)
        ]
        
        # Create expected results test set
        res_set = [
            ("public static", "int", "run_ext_func",
             [["times", "int"]], [], []),
            ("", "void", "print_default_times", [], [], []),
            ("public static", "void", "main", [["args", "String[]"]], [], []),
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().get_method_definition(*test_set[i]), res_set[i]
            )
        
    def test_get_class_definition(self):
        """Test case for Java.get_class_definition"""

        # Create test set
        test_set = [
            (self.file, 1),
            (self.file, 7),
            (self.file, 26)
        ]
        
        # Create expected results test set
        res_set = [
            ("private static", "ParentClass", [], [], [], []),
            ("", "ExtClass", ["ParentClass"],
             ["ParentIntr", "MyIntr"], [], []),
            ("public", "MyProgram", [], [], [], [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().get_class_definition(*test_set[i]), res_set[i]
            )
        
    def test_get_interface_definition(self):
        """Test case for Java.get_interface_definition"""

        # Create test set
        test_set = [
            (self.file, 3),
            (self.file, 5)
        ]
        
        # Create expected results test set
        res_set = [
            ("public static", "ParentIntr", [], [], []),
            ("private", "MyIntr", ["ParentIntr"], [], [])
        ]
        
        # Run test for all tests in test_set
        for i in range(len(test_set)):
        
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().get_interface_definition(*test_set[i]), res_set[i]
            )

    def test_is_if(self):
        """Test case for Java.is_if"""

        # Create test set
        test_set = [
            (self.file, 10),
            (self.file, 14),
            (self.file, 17),
            (self.file, 22)
        ]

        # Create expected results test set
        res_set = [
            True,
            True,
            False,
            False
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().is_if(*test_set[i]), res_set[i]
            )

    def test_is_for(self):
        """Test case for Java.is_for"""

        # Create test set
        test_set = [
            (self.file, 17),
            (self.file, 22),
            (self.file, 28),
            (self.file, 30),
            (self.file, 38),
            (self.file, 33),
            (self.file, 14)
        ]

        # Create expected results test set
        res_set = [
            True,
            True,
            True,
            True,
            True,
            False,
            False
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().is_for(*test_set[i]), res_set[i]
            )

    def test_is_while(self):
        """Test case for Java.is_while"""

        # Create test set
        test_set = [
            (self.file, 33),
            (self.file, 17),
            (self.file, 14)
        ]

        # Create expected results test set
        res_set = [
            True,
            False,
            False
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().is_while(*test_set[i]), res_set[i]
            )

    def test_is_func(self):
        """Test case for Java.is_func"""

        # Create test set
        test_set = [
            (self.file, 9),
            (self.file, 21),
            (self.file, 27),
            (self.file, 26),
            (self.file, 28)
        ]

        # Create expected results test set
        res_set = [
            True,
            True,
            True,
            False,
            False
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().is_func(*test_set[i]), res_set[i]
            )

    def test_is_method(self):
        """Test case for Java.is_method"""

        # Create test set
        test_set = [
            (self.file, 9),
            (self.file, 21),
            (self.file, 27),
            (self.file, 26),
            (self.file, 28)
        ]

        # Create expected results test set
        res_set = [
            True,
            True,
            True,
            False,
            False
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().is_method(*test_set[i]), res_set[i]
            )

    def test_is_cls(self):
        """Test case for Java.is_cls"""

        # Create test set
        test_set = [
            (self.file, 1),
            (self.file, 7),
            (self.file, 26),
            (self.file, 27),
            (self.file, 28)
        ]

        # Create expected results test set
        res_set = [
            True,
            True,
            True,
            False,
            False
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().is_cls(*test_set[i]), res_set[i]
            )

    def test_is_interface(self):
        """Test case for Java.is_interface"""

        # Create test set
        test_set = [
            (self.file, 3),
            (self.file, 5),
            (self.file, 1),
            (self.file, 7),
            (self.file, 26),
            (self.file, 27),
            (self.file, 28)
        ]

        # Create expected results test set
        res_set = [
            True,
            True,
            False,
            False,
            False,
            False,
            False
        ]

        # Run test for all tests in test_set
        for i in range(len(test_set)):
            
            # Test function with inputs and expected outputs
            self.assertEqual(
                Java().is_interface(*test_set[i]), res_set[i]
            )


if __name__ == '__main__':
    unittest.main()
