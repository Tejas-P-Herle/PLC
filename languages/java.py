"""Java language class for conversion to and from java"""
from os import path

from language import Language


class Java(Language):
    def __init__(self, outfile_path="outfile.java"):
        """Initiate Java conversion class"""

        # Set Java class attributes
        self.outfile_name = path.split(outfile_path)[1]
        self.outfile_path = outfile_path
        self.preferred_indent_base = 2
        self.has_semicolon = True
        self.cmnt_chs = ["//", "/*"]

    @staticmethod
    def parse_function_definition(definition, params):
        """Parse function definition and extract useful info"""

        # Dump unwanted portions
        params = params.split(")")[0]
        params = [param.strip() for param in params.split(",")]

        # Set access_modifier to default ""
        access_modifier = ""

        # Split definition at spaces
        def_split = definition.split(" ")

        # Check user input count and match to appropriate variable

        # If 2 variables given, map response to return type and function name
        if len(def_split) == 2:
            return_type, func_name = def_split

        # Else extract all 3 variables from def_split
        else:
            access_modifier, return_type, func_name = (" ".join(def_split[:-2]),
                                                       def_split[-2],
                                                       def_split[-1])

        # Check if parameters are given
        if params == [""]:
            params = []
        else:

            # Split variables to variable name and variable data type
            params = [var.split(" ") for var in params]

            # Remove whitespaces if any and interchange positions
            params = [[var[1].strip(), var[0].strip()] for var in params]

        # Return all variables
        return access_modifier, return_type, func_name, params

    @staticmethod
    def make_function_definition(access_modifier, return_type,
                                 func_name, params):
        """Make function definition from variables"""

        # Make function template
        function_template = "{}{} {}({}) {{"

        # Make parameters string
        params_str = ", ".join([" ".join(param[::-1]) for param in params
                                if param[0] not in ["self"]])

        # If access modifier is given, add space to end of access modifier
        if access_modifier:
            access_modifier += " "

        # Return processed function func_name
        return function_template.format(access_modifier, return_type,
                                        func_name, params_str)

    def convert_if(self, condition, if_kw):
        """Converts if statement to java"""

        # Run super definition
        condition = super().convert_if(condition)

        # Create if template
        if_template = "{if_kw} ({cond}) {{" if condition else "{if_kw} {{"

        # Return converted if statement
        return [if_template.format(if_kw=if_kw, cond=condition)], ["}"]

    def convert_for(self, variable, start, stop, step, array):
        """Converts for statement to java"""

        # Run super definition
        variable, start, stop, step, array = super().convert_for(
            variable, start, stop, step, array
        )

        # Create for template
        for_template = "for ({}) {{{{"

        # Check loop type
        is_for_each = stop == "Array.length"

        # If is for each loop
        if is_for_each:

            # Create for each template
            for_template = for_template.format("{}: {}")

            # Define for_str for loop definition
            for_str = for_template.format(variable, array)

        else:

            # Create for loop template
            for_template = for_template.format("{};{};{}")

            # Define for_str for loop definition
            for_init = "{}{}"
            condition = ""
            var_name = variable.split(" ")[1]

            # Check if start is defined
            if start:
                for_init = for_init.format(variable, " = " + start)

            # Check if stop is defined
            if stop:
                # Assume sign based on step
                sign = ">" if int(step) < 0 else "<"

                # Make condition string
                condition = " {} {} {}".format(var_name, sign, stop)

            # Check if step is provided
            if step:

                # Find sign for increment
                sign = "-" if int(step) < 0 else "+"

                # Check if step is one
                if "1" in step:

                    # If step is one go for shorthand notation
                    step = var_name + sign * 2

                # Else go for long hand
                else:

                    # Make step string
                    step = "{} {}= {}".format(var_name, sign, step)

                # Add space before step to increase readability
                step = " " + step

            for_str = for_template.format(for_init, condition, step)

        # Return converted for statement
        return [for_str], ["}"]

    def convert_while(self, condition):
        """Converts while statement to java"""

        # Run super definition
        condition = super().convert_while(condition)

        # Create if template
        while_template = "while ({cond}) {{"

        # Return converted if statement
        return [while_template.format(cond=condition)], ["}"]

    def convert_function(self, access_modifier, return_type, func_name, params):
        """Converts function definition to java"""

        # Run super func_name
        access_modifier, return_type, func_name, params = \
            super().convert_function(access_modifier, return_type,
                                     func_name, params)

        # In java there are no separate functions all are methods of a class
        return self.convert_method(access_modifier, return_type,
                                   func_name, params)

    def convert_method(self, access_modifier, return_type, func_name, params):
        """Converts method definition to java"""

        # Run super definition
        access_modifier, return_type, func_name, params = \
            super().convert_method(access_modifier, return_type,
                                   func_name, params)

        # Check if is main function
        if func_name == "main" and "public" in access_modifier:

            # If yes, define program class
            # And standard main function signature

            main_class = ["class {} {{".format(
                self.outfile_name.split(".")[0].title())]
            main_fn = ["    public static void main(String[] args) {"]
            end = ["}", "}"]

            # Return main class and main function definition
            return main_class + main_fn, end

        # Make function definition
        func = []
        func += [self.make_function_definition(access_modifier, return_type,
                                               func_name, params)]

        # Return processed function definition
        return func, ["}"]

    def convert_class(self, access_modifier, class_name, classes, interfaces):
        """Converts class definition to java"""

        # Run super definition
        access_modifier, class_name, classes, interfaces = \
            super().convert_class(access_modifier, class_name,
                                  classes, interfaces)

        # Create class template
        class_template = "{}class {}{}{} {{"

        # If access modifier is provided, add space to end for readability
        if access_modifier:
            access_modifier += " "

        # If super classes are provided, make super classes string
        super_cls_str = ""
        if classes:
            # Create super_classes template
            super_cls_str = " extends " + classes[0]

        # Create interfaces string
        intr_str = ""
        if interfaces:
            # Create interfaces string
            intr_str = " implements " + ", ".join(interfaces)

        # Make class definition
        cls_def = class_template.format(access_modifier, class_name,
                                        super_cls_str, intr_str)

        # Return processed class definition
        return [cls_def], ["}"]

    def convert_interface(self, access_modifier, intr_name, interfaces):
        """Converts interface definition to java"""

        # Run super definition
        access_modifier, intr_name, interfaces = super().convert_interface(
            access_modifier, intr_name, interfaces
        )

        # Create interface template
        interface_template = "{}interface {}{} {{"

        # Make interface string
        intr_str = ""

        # Check if any interfaces are provided
        if interfaces:
            # Add java keyword for extending interface
            intr_str += " extends "

            # Add all interfaces to string
            intr_str += ", ".join(interfaces)

        # If access modifier is specified, add space to increase readability
        if access_modifier:
            access_modifier += " "

        # Return processed interface definition
        return [interface_template.format(access_modifier, intr_name,
                                          intr_str)], ["}"]

    def get_if_condition(self, file, i):
        """Gets the condition from if definition"""

        # Run super definition
        line = super().get_if_condition(file, i)

        # Set if keyword for back translation
        ln_split = line.split(" ")
        if ln_split[0] == "else":
            if len(ln_split) > 2 and ln_split[1] == "if":
                if_kw, line = "else if", " ".join(ln_split[2:]).strip()
            else:
                if_kw, line = "else", " ".join(ln_split[1:]).strip()
        else:
            if_kw = "if"

        # Strip start and ending parentheses
        line = line[1:-1]

        # Create start and end for while call
        start = []
        end = []

        # Return if condition
        return line, if_kw, start, end

    def get_for_iterations(self, file, i):
        """Gets number of iterations of for loop"""

        # Run super definition
        definition = super().get_for_iterations(file, i)

        # Check for loop type
        is_for_each = ":" in definition[1]

        # Set variable and array to default(None)
        variable = None
        array = None

        # Check if loop is a for each loop
        if is_for_each:

            # Save split as variable and array
            var_type, variable, array = definition

            # Strip ':' from variable name
            variable = variable.split(":")[0]

            # Merge variable type to variable
            variable = var_type + " " + variable

            # Set begin, stop and step to defaults
            begin, stop, step = 0, "Array.length", 1

        else:

            # Save split at begin, stop, and step
            begin, stop, step = definition

            # Split begin into variable and start
            if begin:
                variable, begin = [part.strip() for part in begin.split("=")]

            # Check for defaults
            if not begin:
                begin = -1

            # Check if default stop
            if not stop:
                stop = -1

            # Else get stop
            else:

                # Store sign for later user if required
                greater_than = False

                # Check if greater than sign is in condition
                if ">" in stop:
                    stop = stop.split(">")[-1]
                    greater_than = True

                # Check if less than sign is in condition
                elif "<" in stop:
                    stop = stop.split("<")[-1]

                # Check if equal sign is in condition
                if "=" in stop:

                    # Strip '=' sign
                    stop = stop.lstrip("=")

                    # Check sign to determine action
                    if greater_than:

                        # If greater than sign, subtract one
                        stop = str(int(stop) - 1)

                    else:

                        # If less than sign, add one
                        stop = str(int(stop) + 1)

                # Strip whitespace if present
                stop = stop.strip()

            # Check if step is provided
            if not step:

                # Set step to default
                step = -1

            else:

                # Check if '=' in step
                if "=" in step:

                    # If found, split '=' and remove whitespaces
                    sign, step = step.split("=")
                    step = step.strip()

                    # Check if negative increment
                    if "-" in sign:
                        step = "-" + step
                else:

                    # Check if negative increment
                    if "-" in step:

                        # Set to step to negative one 
                        step = -1

                    else:

                        # Set step to one 
                        step = 1

        # Create start and end for 'for loop' call
        start = []
        end = []

        # Return all variables
        return variable, str(begin), str(stop), str(step), array, start, end

    def get_while_condition(self, file, i):
        """Gets condition of while loop"""

        # Run super definition
        line = super().get_while_condition(file, i)

        # Strip starting and ending parentheses
        line = line[1:-1]

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
        access_modifier, return_type, func_name, params = \
            self.parse_function_definition(definition, params)

        # Create start and end for function call
        start = []
        end = []

        # Return all variables of function definition
        return access_modifier, return_type, func_name, params, start, end

    def get_method_definition(self, file, i):
        """Gets processed method definition"""

        # Run super definition
        definition, params = super().get_method_definition(file, i)

        # Parse function definition
        access_modifier, return_type, func_name, params = \
            self.parse_function_definition(definition, params)

        # Create start and end for function call
        start = []
        end = []

        # Return all variables of function definition
        return access_modifier, return_type, func_name, params, start, end

    def get_class_definition(self, file, i):
        """Gets processed class definition"""

        # Run super definition
        definition = super().get_class_definition(file, i)

        # Dump unwanted portions
        definition = definition.split("{")[0]

        # Extract class name and superclasses from class definition
        classes = []
        interfaces = []

        # Split definition into access_modifier, class_name
        # And super_class and interfaces
        try:
            access_modifier, definition = definition.split("class ")
        except ValueError:

            # Access_modifiers are not given, set it to default
            access_modifier = ""

        # Remove unwanted whitespace
        access_modifier = access_modifier.strip()

        # Split class name from definition
        def_split = definition.split(" ", 1)

        # Superclass or interfaces are given
        if len(def_split) != 1 and def_split[1] != "":

            # Split definition into class name and super classes and interfaces
            class_name, super_ = def_split

            # Separate super classes(if any) from interfaces
            if super_.find("extends") != -1:
                # Remove extends keyword
                super_ = super_.replace("extends ", "").strip()

                # Split till next space
                classes.append(super_.split(" ")[0])

            # Store interfaces(if any)
            if super_.find("implements") != -1:
                # Remove implements keyword
                super_ = super_.split("implements ")[-1].strip()

                # Split interfaces at ',' and store in list
                interfaces = [intr.strip() for intr in super_.split(",")]

        # Else superclasses or interfaces are not provided
        else:

            # Set split to class name
            class_name = def_split[0]

        # Remove unwanted whitespace
        class_name = class_name.strip()

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
        definition = definition.split("{")[0].strip()

        # Separate access modifier from definition
        try:
            access_modifier, definition = definition.split("interface ")
            access_modifier = access_modifier.strip()
        except ValueError:
            # Access_modifier is not provided, revert to default
            access_modifier = ""

        # Try splitting at open parentheses
        try:
            # Check if interfaces are mentioned
            definition, interfaces = definition.split(" extends ")
            if interfaces:

                # Get all interfaces
                interfaces = [intr.strip() for intr in interfaces.split(",")]

            # Else set interfaces to empty list
            else:
                interfaces = []

        # If failed not interfaces are provided, hence set to empty list
        except ValueError:
            interfaces = []

        # Create start and end for interface call
        start = []
        end = []

        # Rename definition(interface name) to intr_name for readability
        intr_name = definition

        # Return processed interface variables
        return access_modifier, intr_name, interfaces, start, end

    def is_if(self, file, i):
        """Recognizes if line is an if block statement in python"""

        # Save line to local variable
        line = file[i].strip()

        # Check if is else block
        if line[:5] == "else " and line[:7] != "else if":

            # Then return True
            return True

        # If line starts with if and contains ( and )return True, else False
        for delimiter in ["(", ")"]:
            if delimiter not in line:
                return False
        if line[:2] == "if" or line[:7] == "else if":
            return True
        return False

    def is_for(self, file, i):
        """Recognizes if line is a for loop statement in python"""

        # Save line to local variable
        line = file[i].strip()

        # If line starts with for and contains (, ) and { return True, else False
        for delimiter in ["(", ")"]:
            if delimiter not in line:
                return False
        if line.startswith("for"):
            return True
        return False

    def is_while(self, file, i):
        """Recognizes if line is a while loop statement in python"""

        # Save line to local variable
        line = file[i].strip()

        # If line starts with while and contains (, ) and { return True, else False
        for delimiter in ["(", ")"]:
            if delimiter not in line:
                return False
        if line.startswith("while"):
            return True
        return False

    def is_func(self, file, i):
        """Recognize if line is a function definition in python"""

        # Check if line is a method definition as java has no functions
        return self.is_method(file, i)

    def is_method(self, file, i):
        """Recognize if line is a method definition in python"""

        # Save line to local variable
        line = file[i].strip()

        # If line does not contain if, for, while, class and interface
        # and has parentheses and ends with '{' then return True, else False
        for definition in ["if", "for", "while", "class", "interface"]:
            if definition in line:
                return False
        if line.endswith("{"):
            if line.find("(") != -1 and line.find(")") != -1:
                return True
        return False

    def is_cls(self, file, i):
        """Recognize if line is a class definition"""

        # Save line to local variable
        line = file[i].strip()

        # If line contains { and class return True, else False
        if "class " in line and "{" in line:
            return True
        return False

    def is_interface(self, file, i):
        """Recognize if line is an interface definition"""

        # Save line to local variable
        line = file[i].strip()

        # If line contains { and class return True, else False
        if "interface " in line and "{" in line:
            return True
        return False
