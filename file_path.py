"""Parse and manage file_path related functions"""
from os import path
from language import Language


class FilePath:
    def validate_file_path(file_path):
        """Checks if file_path is valid"""
        
        # Check if file exists
        if not path.isfile(file_path):
            return "File - {} Does not exist".format(file_path)
        
        # Get extension from file_path
        extension = Language.recognize(file_path)

        # Check if is supported language source code
        if extension.startswith('Unsupported file extension '):
            return "Unsupported file type"

    def validate_file_name(file_name, input_language):
        """Checks if file_name matches specified language"""

        # Get file extension
        recognized_language = Language.recognize(file_name)

        # Check if file_name extension matches language
        error_message = "Extension and language don't match"
        return None if input_language == recognized_language else error_message

