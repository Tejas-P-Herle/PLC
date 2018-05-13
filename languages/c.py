"""C language class for conversion to and from C"""
from language import Language


class C(Language):
    def if_convert(self, definition): 
        """Converts if statement to C"""
        super().if_convert(definition)
        
    def for_convert(self, definition):
        """Converts for statement to C"""
        super().for_convert(definition) 
    
    def while_convert(self, definition):
        """Converts while statement to C"""
        super().while_convert(definition)
    
    def function_convert(self, definition):
        """Converts function definition to C"""
        super().function_convert(definition)
    
    def class_convert(self, definition):
        """Converts class definition to C"""
        super().class_convert(definition)
    
    def method_convert(self, definition):
        """Converts mathod definition to C"""
        super().method_convert(definition)
    
    def block_convert(self, definition):
        """Converts block statements to C"""
        super().block_convert(definition)

    def get_if_scope(self, definition):
        """Gets scope of if definition"""
        super().get_if_scope(definition)

    def get_for_iterations(self, definition):
        """Gets number of iterations of for loop"""
        super().get_for_iterations(definition)

    def get_function_variable_types(self, definition):
        """Gets type of all variables in function deinition"""
        super().get_function_variable_types(definition)

