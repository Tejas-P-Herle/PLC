"""Process code and act as input to conversion classes"""
from languages.python import Python
from languages.java import Java


class CodeProcessor:
    lang_cls = [Python, Java]

    def __init__(self, file, lang_from, lang_to):
        """Initializes code processor class"""

        # Store input parameters into class attributes
        self.file = file
    
        # Store from and to languages
        self.lang_from = lang_from
        self.lang_to = lang_to

        # Initialize from and to language conversion classes
        self.lang_from_cls = self.lang_cls[lang_from]()
        self.lang_to_cls = self.lang_cls[lang_to]()

        # Make list to store all recognition functions
        recognize_funcs = [self.lang_from_cls.is_if, self.lang_from_cls.is_for,
                           self.lang_from_cls.is_while, self.lang_from_cls.is_func,
                           self.lang_from_cls.is_method, self.lang_from_cls.is_cls,
                           self.lang_from_cls.is_interface]

    def convert(self):
        """Starts conversion of file from language a to language b"""

        # Store file into local variable
        file = self.file

        # Open file for reading
        with open(file) as file:

            # Gets all lines in file as a list
            lines = file.readlines()

            # Iterate over lines in file
            for i in range(lines):

                # Recognize line
                self.recognize_line(lines, i)

    def recognize(self, file, i):
        """Recognize line and segerate into catagories"""
        
        # Run recognition functions to recognize line
        for func in recognize_funcs[:-1]:
            if func(file, i):
                return func.__name__.split("_")[-1]

