"""C language class for conversion to and from C"""
from language import Language


class C(Language):
    def __init__(self, outfile_path="outfile.c"):
        """Initiate C conversion class"""

        # Set C class attributes
        self.outfile_path = outfile_path
        self.preferred_indent_base = 2
        self.has_semicolon = True
