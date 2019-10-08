#!/usr/bin/env python3
"""Get corrections to code made by user for updating conversion tables"""

from regex_gen import RegexGen
from error import Error
import sys


class GetCorrections():

    lns_list = []
    corrections = []

    def __init__(self):
        """Initialize GetCorrections Class"""

        pass


    def append(self, lns):
        """Add line to list of lines to be corrected"""
        
        if lns != ([""],):
            self.lns_list.append("\n".join(ln[0].strip() for ln in lns).strip())


    def remove(self, line):
        """Remove given line form the list"""
        

        # Find line matches
        i = 0
        line = line.strip()
        while len(self.lns_list) > i:

            # Check if the lines match
            if self.lns_list[i] == line:

                # Remove all line matches from list
                self.lns_list.pop(i)
                i -= 1

            # Increment count
            i += 1


    def get(self):
        """Get the corrections for the unknown lines"""
        
        # For line in lines, ask for the conversion
        if self.lns_list:
            print("Please give convert the following lines")

            for ln in self.lns_list:

                print("From Line:", ln)

                # Append corrected lines to list
                self.corrections.append([ln, input("To Line: ")])


    def digest(self, lang_from, lang_to):
        """Learn from the user input corrections"""
        
        # For all corrections found, feed them into regex generator
        for i, ln_pair in enumerate(self.corrections):
            print("{}\nLine From: {}\nLine To: {}\n".format(i, *ln_pair))
            print("ln_pair", *ln_pair)
            print(lang_from, lang_to)
            regex_gen = RegexGen(*ln_pair, lang_from, lang_to)
            if regex_gen.error:
                err_msg = "ERR - GetCorrections: " + str(err)
                print(err_msg, file=sys.stderr)
                Error.parse(err_msg)

