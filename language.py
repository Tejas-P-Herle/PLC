"""Language Class, Super class for all languages"""
from os import path


class Language:
    languages = ['python', 'java', 'cpp', 'c']
    extensions = ['.py', '.java', '.cpp', '.c']
    
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
