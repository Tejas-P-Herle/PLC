"""Python language class for conversion to and from python"""
from language import Language
import re


class Python(Language):
    source_code = []

    def replace_logical_ops(self, line, direction):
        """Replaces all logical operators"""

        # Check if conversion is from or to
        index = 0 if direction == "to" else 1

        # Find list indexes for to and from conversions
        index_a = index
        index_b = (index + 1) % 2
        
        # Create replacement maps
        replacement_list = [["and", "&&", -1], ["or", "||", -1]]

        # Create not replacement list
        not_rep_list = ["not", "!"]

        # Choose not replacement string
        not_rep_str = not_rep_list[index_a]

        # Find indexes for not match string(to and from)
        indexes = [match.start() for match in re.finditer(not_rep_str, line)]
        # Replace not match indexes
        for index in indexes:
            
            # Create not replacement string. Check if space required
            if line[index + len(not_rep_str)] == "(":
                not_rep_list[0] = "not"
            else:
                not_rep_list[0] = "not "

            # Add to replacement list
            # Add in proper order
            not_list = [not_rep_list[index_a], not_rep_list[index_b]]
            replacement_list.append([not_list[index_a], not_list[index_b], 1])
        
        # For operator in operators
        for replacement in replacement_list:

            # Replace with appropriate replacements
            line = line.replace(replacement[index_a], replacement[index_b],
                                replacement[2])
        
        # Return modified line
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

        # Create if template
        if_template = "if {cond}:"

        # Replace logical operators
        condition = self.replace_logical_ops(condition, direction="from")

        # Return converted if statement
        return [if_template.format(cond=condition)]
        
    def convert_for(self, variable, start, stop, step, array):
        """Converts for statement to python"""
        
        # Run super definition
        variable, start, stop, step, array = super().convert_for(
            variable, start, stop, step, array
        )

        # Create for template
        for_template = "for {} in {}:"

        # Define loop condition
        loop_cond = ""
        if array:
            # If array if given, loop through array
            loop_cond = array
            
            # Check if array slicing is required
            if step != "1" or stop != "array.length" or start != "0":

                # Make template for array slicing
                loop_cond = "{}[{{}}]".format(array)

                if start == "0":
                    start = ""

                if stop == "array.length":
                    stop = ""

                if step == "1":
                    step = ""

                # If step is default, omit step
                if not step:

                    # Else add start to range call
                    loop_cond = loop_cond.format(start + ":" + stop)
                else:
                    # Add all three parameters if step is provided
                    loop_cond = loop_cond.format(start + ":" + stop + ":" + step)
 
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

        # Return converted for statement
        return [for_template.format(variable, loop_cond)]
    
    def convert_while(self, condition):
        """Converts while statement to python"""
        
        # Run super definition
        condition = super().convert_while(condition)

        # Make while template
        while_template = "while {cond}:"

        # Replace logical operators
        condition = self.replace_logical_ops(condition, direction="from")

        # Return converted if statement
        return [while_template.format(cond=condition)]
    
    def convert_function(self, access_modifier, return_type, func_name, params):
        """Converts function definition to python"""
        
        # Run super func_name
        line = super().convert_function(access_modifier, return_type,
                                        func_name, params)

        # Make function template
        function_template = "def {}({}) -> {}:"

        # Make parameters string
        params_str = ", ".join([": ".join(param) for param in params])

        # Return processed function func_name
        return [function_template.format(func_name, params_str, return_type)]

    def convert_class(self, access_modifier, class_name, super_classes):
        """Converts class definition to python"""
        
        # Run super definition
        access_modifier, class_name, super_classes = super().convert_class(
            access_modifier, class_name, super_classes
        )

        # Create class template
        class_template = "class {}{}:"

        # If super classes are provided, make super classes string
        super_cls_str = ""
        if super_classes:

            # Create super_classes template
            super_cls_str = "({})"

            # Add all super_classes to sting
            super_cls_str = super_cls_str.format(", ".join(super_classes))

        # Return processed class definition
        return [class_template.format(class_name, super_cls_str)]
    
    def convert_method(self, definition):
        """Converts mathod definition to python"""
        
        # Run super definition
        line = super().convert_method(definition)
    
    def convert_block(self, definition):
        """Converts block statements to python"""
        
        # Run super definition
        line = super().convert_block(definition)

    def convert_decorator(self, definition):
        """Convert python decorator to standard code"""

        # Strip starting '@'
        decorator, function = [part.strip() for part in definition.split("\n")]
        wrapper = decorator.lstrip("@")

        # Get function name
        function_name = self.get_function_definition(function)[2]

        # Create standard code template
        decorator_template = "{0} = {1}({0})".format(function_name, wrapper)

        # Return standard code
        return [decorator_template.format()]

    def get_if_condition(self, definition):
        """Gets the condition from if definition"""
        
        # Run super definition
        line = super().get_if_condition(definition)

        # Strip ending colon
        line = line.rstrip(":")

        # Replace logical operators
        line = self.replace_logical_ops(line, direction="to")

        # Create start and end for while call
        start = []
        end = []
        
        # Return if condition
        return line, start, end

    def get_for_iterations(self, definition):
        """Gets number of iterations of for loop"""
        
        # Run super definition
        line = super().get_for_iterations(definition)
        
        # Save required words
        variable, for_range = line[1], "".join(line[3:])

        # Strip ending semicolon
        for_range = for_range.rstrip(":")

        # Create start and end for 'for loop' call
        start = []
        end = []
        
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
            
            # Set array to None
            array = None
        else:
            # If range not found, iterate over given array

            # Get array
            array = for_range

            # Set default stop
            stop = "arr.length"

            # Check of array slicing
            if array.find("[") != -1 and array.find(":") != -1:
                array, start, stop, step = self.get_list_slice_vars(array)

        # Return all variables
        return variable, start, stop, step, array, start, end


    def get_while_condition(self, definition):
        """Gets condition of while loop"""

        # Run super definition
        line = super().get_while_condition(definition)

        # Strip ending colon
        line = line.rstrip(":")
        
        # Replace logical operators
        line = self.replace_logical_ops(line, direction="to")

        # Create start and end for while call
        start = []
        end = []

        # Return while loop condition
        return line, start, end

    def get_function_definition(self, definition):
        """Gets processed function definition"""
        
        # Run super definition
        definition, params = super().get_function_definition(definition)

        # Sepereate decorator if any
        definition_split = definition.split("\n")
        if len(definition_split) != 1:
            decorator, definition = definition_split

            # Parse decorator
            decorator = convert_decorator

        # Get return value from function definition
        params = params.rstrip(":")
        params, return_type = params.split("->")
        return_type = return_type.strip()
        params = params.strip()
        
        # Dump unwanted portions
        func_name = definition.lstrip("def").strip()
        params = params.rstrip(")")
        params = [param.strip() for param in params.split(",")]

        # Define access modifier
        access_modifier = "private" if func_name.startswith("_") else "public"

        # Create start and end for function call
        start = []
        end = []

        # Seperate annotate of parameter(for variable type)
        params = [param.split(":") for param in params]
       
        # Check if parameters are given
        if params == [[""]]:
            params = []
        else:
            
            # Remove whitespaces if any
            params = [[param[0].strip(), param[1].strip()] for param in params]
    
        # Return all variables of function definition
        return access_modifier, return_type, func_name, params, start, end

    def get_class_definition(self, definition):
        """Gets processed class definition"""

        # Run super definition
        definition = super().get_class_definition(definition)

        # Dump unwanted portions
        definition = definition.rstrip(":")

        # Extract class name and superclasses from class definition
        super_classes = []
        
        # Check if superclass specified
        if definition.find("(") != -1:
            class_name, super_classes = definition.split("(")
            super_classes = super_classes.rstrip(")")
            super_classes = [class_.strip() for class_ in super_classes.split(",")]
        else:
            # If no superclasses specified, extract only classname
            class_name = definition
        
        class_name = class_name.strip()

        # Define access modifier
        access_modifier = "private" if class_name.startswith("_") else "public"

        # Create start and end for class call
        start = []
        end = []
    
        # Return all variables of function definition
        return access_modifier, class_name, super_classes, start, end

    def get_method_definition(self, definition):
        """Gets processed method definition"""
    
        # Run super definition
        definition, params = super().get_method_definition(definition)

