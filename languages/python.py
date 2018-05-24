"""Python language class for conversion to and from python"""
from language import Language
import re


class Python(Language):
    def replace_logical_ops(self, line, direction):
        """Replaces all logical operators"""

        # Find list indexes for to and from conversions
        index_a = 0 if direction == "to" else 1
        index_b = (index_a + 1) % 2
        
        # Create replacement maps
        replacement_list = [["and", "&&"], ["or", "||"], ["not", "!"]]

        # Split line to words list
        words = re.split("([^&|!\w+])", line)

        # Replace logical operators
        i, words_count = 0, len(words)
        while i != words_count:
            
            # Catch exception if index error due to last word
            try:
                # Remove space after 'not'
                if words[i] == "not" and words[i+1] == " " and not index_a:
                    del words[i+1]
                    words_count -= 1

            except IndexError:
                pass

            # Replace words
            for opr in replacement_list:
                if words[i] == opr[index_a]:
                    words[i] = opr[index_b]

            # If '!' is attached with words, replace it with 'not '
            if words[i].startswith("!") and index_a:
                words.insert(i+1, words[i][1:])
                words[i] = "not "

            # Increment count
            i += 1

        # Return modified line
        return "".join(words)

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
            stop = "Array.length"

        # Set step default to 1
        if not step:
            step = "1"

        # Return stripped array with extracted values
        return array, start, stop, step

    def get_type(self, value):
        """Gets type of variable value in python"""

        # Evaluated string statement for type()
        var_type = str(eval("type({})".format(value)))

        # Remove unwanted portions of string
        var_type = var_type.replace("<class '", "").rstrip("'>")

        # Return processed string
        return var_type

    def parse_function_definition(self, file, i, definition, params):
        """Parse function definition and extract useful info"""

        # Save line in local variable definition
        definition = definition.strip()
        params = params.strip()

        # Get return value from function definition
        params = params.rstrip(":")
        try:
            params, return_type = params.split("->")
        except:

            # Default to 'void'
            return_type = "void"
        return_type = return_type.strip().strip("'").strip('"').strip()
        params = params.strip()

        # Dump unwanted portions
        func_name = definition.lstrip("def").strip()
        params = params.rstrip(")")
        params = [param.strip() for param in params.split(",")]

        # Get decorator if any
        decorators = []

        # Initialize j to i
        j = i

        try:

            # While decorators found, add to list
            while file[j-1].strip().startswith("@"):

                # Save decorator line to variable
                decorator = file[j-1].strip()

                # Check if standard decorators
                if decorator in ["@staticmethod", "@classmethod"]:

                    # Save decorators as is(without @)
                    decorators.append(decorator.lstrip("@"))
                else:

                    # Else parse decorator
                    decorators += self.convert_decorator(decorator, func_name)

                # Decrement j
                j -= 1

        # Due to first line in file
        except IndexError:
            pass

        # Seperate annotate of parameter(for variable type)
        params = [param.split(":") for param in params]

        # Check if parameters are given
        if params == [[""]]:
            params = []
        else:

            # Remove whitespaces if any
            params = [[param[0].strip(), param[1].strip()] for param in params]
            
            # Remove quotes for variable type
            params = [[var[0], var[1].strip("'").strip('"')] for var in params]

        # If return type is None with void(return value is type)
        if return_type == "None":
            return_type = "void"

        # Return all variables
        return return_type, func_name, params, decorators

    def make_function_definition(self, return_type, func_name, params):
        """Make function definition from variables"""
        
        # Make function template
        function_template = "def {}({}) -> {!r}:"

        # Close variable type in quotes
        params = [[param[0], "'" + param[1] + "'"] for param in params]

        # Make parameters string
        params_str = ", ".join([": ".join(param) for param in params])

        # If return type is void with None(Python equivalent for void)
        if return_type == "void":
            return_type = "None"

        # Return processed function func_name
        return function_template.format(func_name, params_str, return_type)

    def get_class_name(self, file, i):
        """Gets first previously parsed class"""

        # Iterate over file but backwards
        for j in range(i, -1, -1):
            
            # Check if line is a class definition
            if self.is_cls(file, j):
                
                # Store line in local variable
                line = file[j].rstrip(":")

                # Get class name
                class_name = line.replace("class", "").strip().split("(")[0]

                # Return class name
                return class_name.strip()

    def get_doc_str(self, file, i):
        """Returns doc string of object"""

        # Save triple double and single quotes in variables
        single_quotes = "'" * 3
        double_quotes = '"' * 3
        quotes = None
        j = -1
        doc_str = []

        # Search first occurance of triple quotes
        for j in range(i, len(file)):

            if single_quotes in file[j]:

                # Append doc string line to doc_str list
                doc_str.append(file[j].strip().strip("'"))
                if file[j].count(single_quotes) == 2:

                    # Is a one line doc_str
                    return doc_str
                
                # Quotes to single quotes
                quotes = single_quotes

            elif double_quotes in file[j]:

                # Append doc string line to doc_str list
                doc_str.append(file[j].strip().strip('"'))
                if file[j].count(double_quotes) == 2:

                    # Is a one line doc_str
                    return doc_str
                
                # Quotes to double quotes
                quotes = double_quotes

            # If first set of quotes are fount set j and break from loop
            if quotes:
                j += 1
                break

        # While ending quotes not found add string to doc_string
        while quotes not in file[j]:

            # Add line to doc_str and increment line pointer
            doc_str.append(file[j].strip().strip(quotes))
            j += 1

        # Add closing line to docstring and return result
        doc_str.append(file[j].strip().strip(quotes))
        return doc_str
        
    def convert_if(self, condition): 
        """Converts if statement to python"""
        
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

        # Remove data type from variable(duck typing in Python)
        variable = variable.split(" ")[-1]

        # Create for template
        for_template = "for {} in {}:"

        # Define loop condition
        loop_cond = ""
        if array:
            # If array if given, loop through array
            loop_cond = array
            
            # Check if array slicing is required
            if step != "1" or stop != "Array.length" or start != "0":

                # Make template for array slicing
                loop_cond = "{}[{{}}]".format(array)

                if start == "0":
                    start = ""

                if stop == "Array.length":
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
        access_modifier, return_type, func_name, params =\
            super().convert_function(access_modifier, return_type,
                                        func_name, params)

        # Make and return processd function definition
        return [self.make_function_definition(return_type, func_name, params)]

    def convert_method(self, access_modifier, return_type, func_name, params):
        """Converts mathod definition to python"""
        
        # Run super definition
        access_modifier, return_type, func_name, params =\
            super().convert_method(access_modifier, return_type,
                                   func_name, params)

        # Make function definition
        function = []
        function += [self.make_function_definition(return_type,
                                                  func_name, params)]

        # Add decorator if required
        if "static" in access_modifier:
            function.insert(0, "@staticmethod")

        # Return processed function definition
        return function

    def convert_class(self, access_modifier, class_name, classes, interfaces):
        """Converts class definition to python"""
        
        # Run super definition
        access_modifier, class_name, classes, interfaces =\
            super().convert_class(access_modifier, class_name,
                                  classes, interfaces)

        # Merge classes and interfaces both are the same in python
        super_ = classes + interfaces

        # Create string to denote super name as interface
        dnt = ": interface"

        # Create docstring
        doc_str = [name+dnt for name in interfaces]

        # Create class template
        class_template = "class {}{}:"

        # If super classes are provided, make super classes string
        super_cls_str = ""
        if super_:

            # Create super_classes template
            super_cls_str = "({})"

            # Add all super_classes to sting
            super_cls_str = super_cls_str.format(", ".join(super_))

        # If doc string is not empty add starting and ending quotes to docstring
        if doc_str:
            doc_str[0] = '"""' + doc_str[0]
            doc_str[-1] += '"""'

        # Return processed class definition
        return [class_template.format(class_name, super_cls_str)] + doc_str

    def convert_interface(self, interface_name, interfaces):    
        """Converts interface definiton to python"""

        # Run super definition
        interface_name, interfaces = super().convert_interface(
            interface_name, interfaces
        )

        # Set access modifier to public(interfaces are always public)
        access_modifier = "public"

        # Run class converter(interface and classes are the same in python)
        class_def = self.convert_class(
            access_modifier, interface_name, [], interfaces
        )

        # Add class type to docstring to denote interface
        intr_def, doc_str = class_def[0], class_def[1:]
        intr_dnt = "class type: interface"

        # Add new line if docstring has seperate text
        if doc_str:

            # Remove statring quotes
            quotes = doc_str[0][:3]
            doc_str[0] = doc_str[0][3:]

            # Insert text into first line
            doc_str.insert(0, quotes + intr_dnt)
        else:
            doc_str = ['"""' + intr_dnt + '"""']

        # Return processed interface definition
        return [intr_def] + doc_str
    
    def convert_decorator(self, decorator, func_name):
        """Convert python decorator to standard code"""

        # Strip starting '@'
        wrapper = decorator.lstrip("@")

        # Create standard code template
        decorator_template = "{0} = {1}({0})".format(func_name, wrapper)

        # Return standard code
        return [decorator_template.format()]

    def get_if_condition(self, file, i):
        """Gets the condition from if definition"""
        
        # Run super definition
        line = super().get_if_condition(file, i)

        # Strip ending colon
        line = line.rstrip(":")

        # Replace logical operators
        line = self.replace_logical_ops(line, direction="to")

        # Create start and end for while call
        start = []
        end = []
        
        # Return if condition
        return line, start, end

    def get_for_iterations(self, file, i):
        """Gets number of iterations of for loop"""
        
        # Run super definition
        line = super().get_for_iterations(file, i)
        
        # Save required words
        variable, for_range = line[0], "".join(line[2:])

        # Strip ending semicolon
        for_range = for_range.rstrip(":")

        # Create start and end for 'for loop' call
        start = []
        end = []
        
        # Set start and step to default
        begin = "0"
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
            # Set stop variable with default begin and step
            if var_count == 1:
                stop = variables[0]
            # Else if two variable are given,
            # set begin and stop variable with default step
            else:
                begin = variables[0]
                stop = variables[1]
                # If three variables are given,
                # set all three begin, stop and step variables
                if var_count == 3:
                    step = variables[2]
            
            # Set array to None
            array = None
        else:
            # If range not found, iterate over given array

            # Get array
            array = for_range

            # Set default stop
            stop = "Array.length"

            # Check of array slicing
            if array.find("[") != -1 and array.find(":") != -1:
                array, begin, stop, step = self.get_list_slice_vars(array)

        # Get variable type for variable

        # If array is passed, get type of array
        if array:
            var_type = "Array.data_type"

        # Else get type of variable
        else:
            var_type = self.get_type(begin)

        # Append variable type to variable
        variable = var_type + " " + variable

        # Return all variables
        return variable, begin, stop, step, array, start, end


    def get_while_condition(self, file, i):
        """Gets condition of while loop"""

        # Run super definition
        line = super().get_while_condition(file, i)

        # Strip ending colon
        line = line.rstrip(":")
        
        # Replace logical operators
        line = self.replace_logical_ops(line, direction="to")

        # Create start and end for while call
        start = []
        end = []

        # Return while loop condition
        return line, start, end

    def get_function_definition(self, file, i):
        """Gets processed function definition"""
        
        # Run super definition
        definition, params = super().get_function_definition(file, i)

        # Parse function definition
        return_type, func_name, params, decorator =\
            self.parse_function_definition(file, i, definition, params)

        # Define access modifier
        is_private = func_name.startswith("__") and func_name.count("__") < 2
        access_modifier = "private" if is_private else "public"

        # Create start and end for function call
        start = []
        end = [] + decorator
    
        # Return all variables of function definition
        return access_modifier, return_type, func_name, params, start, end

    def get_method_definition(self, file, i):
        """Gets processed method definition"""
    
        # Run super definition
        definition, params = super().get_method_definition(file, i)

        # Get class name
        class_name = self.get_class_name(file, i)

        # Parse function definition
        return_type, func_name, params, decorator =\
            self.parse_function_definition(file, i, definition, params)

        # Define access modifier
        is_private = func_name.startswith("__") and func_name.count("__") < 2
        access_modifier = "private" if is_private else "public"

        # Create start and end for function call
        start = []
        end = []

        # Check if decorator states static method or class method
        if "staticmethod" in decorator:
            access_modifier += " static"
        elif "classmethod" in decorator:
           start += [params[0][0] + " = " + class_name]
    
        # Return all variables of function definition
        return access_modifier, return_type, func_name, params, start, end

    def get_class_definition(self, file, i):
        """Gets processed class definition"""

        # Run super definition
        definition = super().get_class_definition(file, i)

        # Get docstring from definition
        definition, docstring = definition.rsplit("\n", 1)

        # Dump unwanted portions
        definition = definition.rstrip(":")

        # Define storage lists
        classes = []
        interfaces = []
        super_list = [classes, interfaces]
        
        # Check if superclass or interfaces specified
        if definition.find("(") != -1:

            # Extract class name and superclasses from class definition
            class_name, super_ = definition.split("(")
            super_ = super_.rstrip(")")

            # Store all superclasses and interfaces to list
            super_split = [part.strip() for part in super_.split(",")]
            for super_ in super_split:

                # Set default to super class
                index = 0

                # Get superclass or interface name start in docstring
                var_loc = docstring.find(super_)

                # Check if name found in docstring and specifies interface
                if var_loc != -1:
                    
                    # Get location of specification
                    spec_loc = var_loc + len(super_) + len(": ")

                    # Check if interface is specified
                    intr_str = "interface"
                    if docstring[spec_loc: spec_loc+len(intr_str)] == intr_str:
                        
                        # Change specification to interface
                        index = 1

                # Add superclass or interface name to appropriate list
                super_list[index] += [super_]

        else:
            
            # If no superclasses specified, extract only classname
            class_name = definition
        
        # Strip whitespace
        class_name = class_name.strip()

        # Define access modifier
        is_private = class_name.startswith("__") and class_name.count("__") < 2
        access_modifier = "private" if is_private else "public"

        # Create start and end for class call
        start = []
        end = []
    
        # Return all variables of function definition
        return access_modifier, class_name, classes, interfaces, start, end

    def get_interface_definition(self, file, i):
        """Gets processed interface definition"""

        # Run super definition
        definition = super().get_interface_definition(file, i)

        # Dump unwanted portions
        definition = definition.lstrip("class ")
        definition = definition.rstrip(":").rstrip(")").strip()

        # Try splitting at open parentheses
        try:
            # Check if interfaces are mentioned
            definition, interfaces = definition.split("(")
            if interfaces:
                
                # Get all interfaces
                interfaces = [intr.strip() for intr in interfaces.split(",")]

            # Else set interfaces to empty list
            else:
                interfaces = []


        # If failed not inerfaces are provided, hence set to empty list
        except ValueError:
            interfaces = []

        # Create start and end for interface call
        start = []
        end = []

        # Return processed interface name
        return definition, interfaces, start, end

    def is_if(self, file, i):
        """Recognizes if line is an if block statement in python"""

        # Save line to local variable
        line = file[i]
        
        # If line starts with if and ends with ':' return True, else False
        if line.startswith("if") and line.endswith(":"):
            return True
        return False

    def is_for(self, file, i):
        """Recognizes if line is a for loop statement in python"""

        # Save line to local variable
        line = file[i]

        # If line starts with for and ends with ':' return True, else False
        if line.startwith("for") and line.endswith(":"):
            return True
        return False

    def is_while(self, file, i):
        """Recognizes if line is a while loop statement in python"""

        # Save line to local variable
        line = file[i]

        # If line starts with while and ends with ':' return True, else False
        if line.startswith("while") and line.endswith(":"):
            return True
        return False

    def is_func(self, file, i):
        """Recognize if line is a function definition in python"""

        # Save line to local variable
        line = file[i]
        
        # If line starts with 'def' and has parentheses and ends with ':'
        # Then return True, else False
        if line.startswith("def") and line.endswith(":"):
            if line.find("(") != -1 and line.find(")") != -1:
                return True
        return False

    def is_method(self, file, i):
        """Recognize if line is a method definition in python"""

        # Save line to local variable
        line = file[i]

        # Check if line is a function definition as method is also a function
        # Note: Don't run is_func() if line found inside class
        return self.is_func(line)

    def is_cls(self, file, i):
        """Recognize if line is a class definition"""

        # Save line to local variable
        line = file[i]

        # If line starts with 'class' and ends with ':' return True, else False
        if line.startswith("class ") and line.endswith(":"):
            return True
        return False

    def is_interface(self, file, i):  
        """Recognize if line is an interface definition"""

        # Save line to local variable
        line = file[i]

        # Get doc_str for class
        doc_str = self.get_doc_str(file, i)

        # If line matches class definition and doc_string specifies interface
        # Then return True, else False
        if self.is_cls(line) and "class type: interface" in doc_str:
            return True
        return False

