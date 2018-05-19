"""Language Class, Super class for all languages"""
from os import path


class Language:
    languages = ['python', 'java', 'cpp', 'c']
    extensions = ['.py', '.java', '.cpp', '.c']
    source_code = []
    
    @classmethod
    def get_language(cls, extension):
        """Get corresponding language for extension"""
        # Check if extension is a string
        if not isinstance(extension, str):
            return (None, "Parameter extension must be a string")
        
        try:
            # Try to return corresponding language
            return dict(zip(cls.extensions, cls.languages))[extension.lower()]
        except KeyError:
            # If unknown extension, return error
            return (None, "Unsupported file extension {}".format(extension))

    @classmethod
    def recognize(cls, file_path):
        """Recognize file language from file path"""
        
        # Check if file_path is a string
        if not isinstance(file_path, str):
            return (None, "Parameter file_path must be a string")
        
        # Get Extension from file_path
        extension = path.splitext(file_path.lower())[1]
        
        # Return corresponding language or error
        return cls.get_language(extension)

    @classmethod
    def validate(cls, language):
        """Check if language is supported"""

        # Check if language is a string
        if not isinstance(language, str):
            return "Parameter language must be a string"

        # Check for language in supported languages
        try:
            cls.languages.index(language.lower())
            
            # Return None (No Error) if language exists in supported languages
            return None
        except ValueError:

            # Else return unsupported language
            return "Unsupported language {}".format(language)

    def convert_if(self, condition):
        """Converts if defenition"""
        
        # Return processed condition
        return condition

    def convert_for(self, variable, start, stop, step, array):
        """Converts for definition"""
        
        # Return processed 'for variables'
        return variable, start, stop, step, array

    def convert_while(self, condition):
        """Converts while definition"""
        
        # Return processed condition
        return condition

    def convert_function(self, access_modifier, return_type,
                         func_name, params):
        """Converts function definition"""
        
        # Return processed function variables
        return access_modifier, return_type, func_name, params

    def convert_block(self, block):
        """Converts all lines of code except definitions"""
        pass

    def convert_class(self, access_modifier, class_name, super_classes):
        """Converts class definition"""
        
        # Return processed class variables
        return access_modifier, class_name, super_classes

    def convert_method(self, definition):
        """Converts method of class"""
        pass

    def get_if_condition(self, definition):
        """Gets if condition from definition"""
        
        # Get raw if condition
        line = definition.lstrip("if")
        
        # Remove curly braces if present
        line = line.strip("{")
        
        # Remove whitespace
        line = line.strip()

        # Return if condition
        return line

    def get_for_iterations(self, definition):
        """Gets number of iterations of for loop"""
        
        # Break line into sub pieces
        word_split = definition.split(' ')
        has_semicolon = definition.find(';') != -1
        semicolon_split = definition.split(';')
        return semicolon_split if has_semicolon else word_split

    
    def get_while_condition(self, definition):
        """Gets condition of while loop"""
        
        # Get raw while condition
        line = definition.lstrip("while")

        # Remove curly braces if present
        line = line.strip("{")
        
        # Remove whitespaces
        line = line.strip()

        # Return while condition
        return line

    def get_function_definition(self, definition):
        """Gets processed function definition"""
        
        # Find opening parentheses for fuction parameters
        index = definition.find("(")

        # Split at opening parentheses
        definition, params = definition[:index], definition[index+1:]

        # Return definition and parameters
        return definition, params

    def get_class_definition(self, definition):
        """Gets processed class definition"""

        # Dump unwanted 'class' keyword
        definition = definition.lstrip("class").strip()

        # Return processed definition
        return definition

    def get_method_definition(self, definition):
        """Gets processed method definition"""
        
        # Parse as a function (Methods are also functions)
        definition, params = get_function_definition(definition)

        # Return processed definition
        return definition, params

