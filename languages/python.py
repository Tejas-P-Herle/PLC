"""Python language class for conversion to and from python"""
from language import Language


class Python(Language):
    def if_convert(self, definition): 
        """Converts if statement to python"""
        
        # Run super definition
        line = super().if_convert(definition)

        # Strip ending colon
        line = line.rstrip(":")

        # Replace and, or conditions
        line = line.replace("and", "&&")
        line = line.replace("or", "||")
        
        # Replace not condition
        # Count whitespace after 'not'
        whitespace = 0
        index = line.find("not") + 2
        if index != -1:
            while line[index + 1] == " ":
                whitespace += 1
                index += 1
        
        # Replace not and whitespace/s with '!'
        line = line.replace("not" + " " * whitespace, "!")
        
        # Return if condition
        return line
        
    def for_convert(self, definition):
        """Converts for statement to python"""
        super().for_convert(definition) 
    
    def while_convert(self, definition):
        """Converts while statement to python"""
        super().while_convert(definition)
    
    def function_convert(self, definition):
        """Converts function definition to python"""
        super().function_convert(definition)
    
    def class_convert(self, definition):
        """Converts class definition to python"""
        super().class_convert(definition)
    
    def method_convert(self, definition):
        """Converts mathod definition to python"""
        super().method_convert(definition)
    
    def block_convert(self, definition):
        """Converts block statements to python"""
        super().block_convert(definition)

    def get_if_scope(self, definition):
        """Gets scope of if definition"""
        super().get_if_scope(definition)

    def get_for_iterations(self, definition):
        """Gets number of iterations of for loop"""
        
        # Run super definition
        line = super().get_for_iterations(definition)
        
        # Save required words
        variable, for_range = line[1], "".join(line[3:])

        # Parse for_range
        if for_range.find("range") != -1:
            
            # Set start and step to default
            start = 0
            step = 1
            
            # Dump unwanted portion
            for_range = for_range.strip("range(").strip(")")

            # Parse variables in for_range
            variables = [var.strip() for var in for_range.split(",")]

            # Store variable values
            var_count = len(variables)
            
            # If only one variable is given,
            # Return stop variable with default start and step
            if var_count == 1:
                return start, variables[0], step
            # Else if two variable are given,
            # Return start and stop variable with default step
            elif var_count == 2:
                return variables[0], variables[1], step
            # Else three variables are given,
            # Return all three start, stop and step variables
            else:
                return variables[0], variables[1], variables[2]
        else:
            return "Under development", variable, for_range

    def get_function_variable_types(self, definition):
        """Gets type of all variables in function deinition"""
        super().get_function_variable_types(definition)

