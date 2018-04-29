"""Parse and manage file_path related functions"""
from os import path
from language import Language


class FilePath:

    def validate_file_path(file_path):
        """Checks if file_path is valid"""

        # Check if file_path is a string
        if not isinstance(file_path, str):
            return "Parameter file_path must be a string"

        # Check if user requests quit action
        if file_path == "q":
            return "User Abort"
        
        # Check if file exists
        if not path.isfile(file_path):
            return "File - {} Does not exist".format(file_path)
        
        # Get extension from file_path
        response = Language.recognize(file_path)

        # Check if error encountered
        if isinstance(response, list) and response[0] == None:
            
            # Parse error
            Error.parse(response)

        # Else save response
        extension = response

        # Check if is supported language source code
        if extension.startswith('Unsupported file extension '):
            return "Unsupported file type"

    def validate_file_name(file_name, input_language):
        """Checks if file_name matches specified language"""

        # Check if file_name and input_language are strings
        if not (isinstance(file_name, str) and isinstance(input_language, str)):
            return "Parameters file_name and input_language must be a string"

        # Check if user requests quit action
        if file_name == "q":
            return "User Abort"
        
        # Get file extension
        response = Language.recognize(file_name)

        # Check if error encountered
        if isinstance(response, list) and response[0] == None:
            
            # Parse error
            Error.parse(response)

        # TODO Check if file_name is a valid

        # Else save response
        recognized_language = response

        # Check if file_name extension matches language
        error_message = "Extension and language don't match"
        
        # Return validation result
        if input_language != recognized_language:
            return error_message

