"""Python language class for conversion to and from python"""
from language import Language


class Python(Language):
    python_source_code = []

    def replace_logical_ops(self, line):
        """Replaces all logical operators"""

        # Replace and, or operators
        line = line.replace("and", "&&")
        line = line.replace("or", "||")
        
        # Replace not operator
        not_str = "not" if line[line.find("not") + 3] == "(" else "not "

        # Replace 'not' and whitespace/s with '!', return result
        line = line.replace(not_str, "!")
        return line

    def if_convert(self, definition): 
        """Converts if statement to python"""
        super().if_convert(definition)        
        
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

    def get_if_condition(self, definition):
        """Gets the condition from if definition"""
        
        # Run super definition
        line = super().get_if_condition(definition)

        # Strip ending colon
        line = line.rstrip(":")

        # Replace logical operators
        line = self.replace_logical_ops(line)

        # Return if condition
        return line

    def get_if_scope(self, definition):
        """Gets scope of if definition"""
        super().get_if_scope(definition)

    def get_for_iterations(self, definition):
        """Gets number of iterations of for loop"""
        
        # Run super definition
        line = super().get_for_iterations(definition)
        
        # Save required words
        variable, for_range = line[1], "".join(line[3:])

        # Strip ending semicolon
        for_range = for_range.rstrip(":")
        
        # Set start and step to default
        start = 0
        step = 1

        # Parse for_range
        if for_range.find("range") != -1:
            
            # Dump unwanted portion
            for_range = for_range.strip("range(").strip(")")

            # Parse variables in for_range
            variables = [var.strip() for var in for_range.split(",")]

            # Store variable values
            var_count = len(variables)
            
            # If only one variable is given,
            # Set stop variable with default start and step
            if var_count == 1:
                stop = variables[0]
            # Else if two variable are given,
            # set start and stop variable with default step
            else:
                start = variables[0]
                stop = variables[1]
                # If three variables are given,
                # set all three start, stop and step variables
                if var_count == 3:
                    step = variables[2]
            
            # Return all four variables, including array(None in this case)
            array = None
            return variable, start, stop, step, array
        else:
            # If range not found, iterate over given array

            # Get array
            array = for_range

            # Set stop
            stop = "arr.length"

            # Return all four variables, including array
            return variable, start, stop, step, array


    def get_while_condition(self, definition):
        """Gets condition of while loop"""

        # Run super definition
        line = super().get_while_condition(definition)

        # Strip ending colon
        line = line.rstrip(":")
        
        # Replace logical operators
        line = self.replace_logical_ops(line)

        # Return while loop condition
        return line

    def get_function_definition(self, definition):
        """Gets processed function definition"""
        
        # Run super definition
        definition, params = super().get_function_definition(definition)

        # Define access modifier
        access_modifier = "public"

        # Get return value from function definition
        params = params.rstrip(":")
        params, return_val = params.split("->")
        return_val = return_val.strip()
        params = params.strip()
        
        # Dump unwanted portions
        definition = definition.lstrip("def ")
        params = params.rstrip(")")
        params = [param.strip() for param in params.split(",")]

        # Seperate annotate of parameter(for variable type)
        params = [param.split(":") for param in params]

        # Remove whitespaces if any
        params = [[param[0].strip(), param[1].strip()] for param in params]
    
        # Return all variables of function definition
        return access_modifier, return_val, definition, params

