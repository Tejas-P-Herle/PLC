"""Python language class for conversion to and from python"""
from language import Language


class Python(Language):
    source_code = []

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

    def get_list_slice_vars(self, list_):
        """Gets the start, stop and step from a list sliceing call"""

        # Dump unwanted portions
        array, list_ = list_.split("[")
        list_ = list_.rstrip("]")

        # Split at ':'
        variables = list_.split(":")
        var_count = len(variables)

        start = ""
        stop = ""
        step = ""

        # If step provided
        if var_count == 3:
            
            # If provided, store provided values
            start, stop, step = variables
        else:

            # Else store start, stop with default step
            start, stop = variables

        # If values are not provided by user, fall back to defaults
        
        # Set start default to 0
        if not start:
            start = "0"

        # Set stop default to array length
        if not stop:
            stop = "array.length"

        # Set step default to 1
        if not step:
            step = "1"

        # Return stripped array with extracted values
        return array, start, stop, step

    def convert_if(self, condition): 
        """Converts if statement to python(vital condition to be provided)"""
        
        # Run super definition
        condition = super().convert_if(condition)

        # Add converted if statement to source code
        self.source_code.append("if {cond}:".format(cond=condition))
        
    def convert_for(self, variable, start, stop, step, array):
        """Converts for statement to python"""
        
        # Run super definition
        variable, start, stop, step, array = super().convert_for(
            variable, start, stop, step, array
        )

        # Define loop condition
        loop_cond = ""
        if array:
            # If array if given, loop through array
            loop_cond = array

            # If step is default, omit step
            if step == "1":
                pass
        else:
            # Else make range template
            loop_cond = "range({})"

            # If step if default, omit step
            if step == "1":
                
                # If start is default, omit start
                if start == "0":
                    loop_cond = loop_cond.format(stop)
                
                else:
                    # Else add start to range call
                    loop_cond = loop_cond.format(start + ", " + stop)
            else:
                # Add all three parameters if step is provided
                loop_cond = loop_cond.format(start + ", " + stop + ", " + step)

        # Add converted for statement to source code
        self.source_code.append("for {} in {}:".format(variable, loop_cond))
    
    def convert_while(self, definition):
        """Converts while statement to python"""
        
        # Run super definition
        line = super().convert_while(definition)
    
    def convert_function(self, definition):
        """Converts function definition to python"""
        
        # Run super definition
        line = super().convert_function(definition)
    
    def convert_class(self, definition):
        """Converts class definition to python"""
        
        # Run super definition
        line = super().convert_class(definition)
    
    def convert_method(self, definition):
        """Converts mathod definition to python"""
        
        # Run super definition
        line = super().convert_method(definition)
    
    def convert_block(self, definition):
        """Converts block statements to python"""
        
        # Run super definition
        line = super().convert_block(definition)

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

    def get_for_iterations(self, definition):
        """Gets number of iterations of for loop"""
        
        # Run super definition
        line = super().get_for_iterations(definition)
        
        # Save required words
        variable, for_range = line[1], "".join(line[3:])

        # Strip ending semicolon
        for_range = for_range.rstrip(":")
        
        # Set start and step to default
        start = "0"
        step = "1"

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

            # Set default stop
            stop = "arr.length"

            # Check of array slicing
            if array.find("[") != -1 and array.find(":") != -1:
                array, start, stop, step = self.get_list_slice_vars(array)

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

