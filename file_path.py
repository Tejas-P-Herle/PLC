"""Parse and manage file_path related functions"""
from os import path
from language import Language
from error import Error


class FilePath:
    @staticmethod
    def validate_file_path(file_path):
        """Checks if file_path is valid"""

        # Check if file_path is a string
        if not isinstance(file_path, str):
            return "Parameter file_path must be a string"
        
        # Check if file exists
        if not path.isfile(file_path):
            return "File - {} Does not exist".format(file_path)
        
        # Get extension from file_path
        response = Language.recognize(file_path)

        # Check if error encountered
        if isinstance(response, tuple) and not response[0]:
            
            # Parse error
            Error.parse(response)

            # Save error response
            extension = response[1]

        else:
            # Else save response
            extension = response

        # Check if is supported language source code
        if extension.startswith('Unsupported file extension '):
            return "Unsupported file type"

    @staticmethod
    def validate_file_name(file_name, input_language):
        """Checks if file_name matches specified language"""

        # Check if file_name and input_language are strings
        if not (isinstance(file_name, str) and isinstance(input_language, str)):
            return "Parameters file_name and input_language must be a string"
        
        # Get file extension
        response = Language.recognize(file_name)

        # Check if error encountered
        if isinstance(response, list) and not response[0]:
            
            # Parse error
            Error.parse(response)

        # Check if file_name is a valid
        special_characters = "\\/:*?\"<>|"
        for character in special_characters:
            if file_name.find(character) != -1:
                return "File name must not contain '%s'" % special_characters

        # Else save response
        recognized_language = response

        # Check if file_name extension matches language
        error_message = "Extension and language don't match"
        
        # Return validation result
        if input_language != recognized_language:
            return error_message

