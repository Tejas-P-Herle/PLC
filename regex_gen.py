
SIGNS = "!@#$%^&*()_+-={}[]|\\:;\"'<>?,./~`"
ESCAPE_CHARS = "+*?^$\.[]{}()|/"


class RegexGen:

    db_files = {"python": "py_conv_db.db", "java": "java_conv_db.db"}
    match_dict = {}
    diff_dict = {}
    escape_chars = ["+", "(", ")", "\\"]

    def __init__(self, line_from_ex_set, line_to_ex_set):
        
        # Store as class attributes and escape required characters
        # Iterate over all characters in the lines in examples set
        for line_from, line_to in zip(line_from_ex_set, line_to_ex_set):
            self.line_from, self.line_to = line_from, line_to

            # Get difference between lines
            self.get_diff()

        # Generate regex for input language
        self.regex_from = self.gen_regex()

        # Reset difference dictionary and match dictionary
        self.diff_dict = {}
        self.match_dict = {}

        # Iterate over all characters in the lines in examples set
        for line_from, line_to in zip(line_from_ex_set, line_to_ex_set):
            # Replace line from and line to
            self.line_from, self.line_to = line_to, line_from

            # Get difference between lines
            self.get_diff()

        # Generate regex for output language
        self.regex_to = self.gen_regex()

    def get_diff(self):
        """Get difference between two strings"""

        # Define dict to store difference and int to store char location
        diff_dict = self.diff_dict
        match_dict = self.match_dict
        i = 0

        # Find matches and differences in strign
        while i < len(self.line_from):

            # Find difference starting from character at index i
            match = self.find_str_match(i + 1, self.line_from[i])

            # Store length of match
            len_match = len(match)

            # Check if lenght of match is one
            if len_match == 1:

                # Escape character if required
                if match in ESCAPE_CHARS:
                    match = "\\" + match

                # If yes, store in difference dict
                diff_dict[i] = match
            else:

                # Get start and end of match
                index = self.line_to.index(match)
                index = index, index + len_match

                # Else store in match dict
                match_dict[(i, i + len_match)] = index, match

            # Increment count
            i += len_match

        # Store list as class attributes
        self.match_dict = match_dict
        self.diff_dict = diff_dict

    def find_str_match(self, i, sub_str):
        """Find character to character match in string starting from i"""

        # Check if next index exists
        if i < len(self.line_from):

            # Make new substring
            new_str = sub_str + self.line_from[i]

        # Else return sub_str
        else:
            return sub_str

        # Check if current string is in line_to
        if new_str not in self.line_to:

            # Return till current match
            return sub_str
        else:

            # Return find match of new substring
            return self.find_str_match(i+1, sub_str + self.line_from[i])

    def gen_regex(self):
        """Generate regex given differences and matches between strings"""

        # Define regex and index to store index and
        regex = ""
        i = 0

        # Run a while loop through all elements of the array
        while i in range(len(self.line_from)):

            # Iterate through all elements in differences dict
            # And check if current index in difference dict
            if i in self.diff_dict.keys():

                # Check if character is to be escaped
                if self.line_from[i] in self.escape_chars:

                    # Then add a preceding backslash
                    regex += "\\"

                # If yes, then copy text from start to end of diff
                regex += self.line_from[i]
            
            # Else it is in match list
            else:

                # Iterate through all ranges in match dictionary
                for rng in self.match_dict.keys():

                    # Check if current index is range start
                    if i == rng[0]:

                        # Then get next anticipated character
                        # Set default next anticipated character to white space
                        nxt_char = "\\n" if rng[1] == len(self.line_from) else ""

                        # Iterate through difference dict and check indexes
                        for j, char in self.diff_dict.items():
                            
                            # If index is greater than current character
                            # Then set it as next anticipated character
                            if i < j and char.strip():
                                nxt_char = char
                                
                                # Break out of loop to stop at immediate next character
                                break

                        # Check if next character is a null string
                        if nxt_char:

                            # Set regex to accept all characters
                            # Except next anticipated character
                            regex += "([^{}])*".format(nxt_char)

                        else:

                            # If is null string, get super sets for substring
                            super_sets = self.find_super_set(
                                self.line_from[rng[0]: rng[1]])

                            possible_matches = "(["
                            
                            # For super set add possible match
                            if super_sets & 1:

                                # If is an alphabet, add [a-z] to matches
                                possible_matches += "a-z"
                            
                            if super_sets & 2:
                                
                                # If is an alphabet(upper), add [A-Z] to matches
                                possible_matches += "A-Z"
                            
                            if super_sets & 4:
                                
                                # If is an number, add [0-9] to matches
                                possible_matches += "0-9"

                            if super_sets & 8:

                                # If has whitespace space(' '), add ' ' to matches
                                possible_matches += " "

                            if super_sets & 16:
                                # If is a sign, add all signs to matches
                                possible_matches += SIGNS.replace("\\", "\\\\").replace("-", "\-").replace("]", "\]")

                            possible_matches += "])"

                            # Check if possible matches is all or null
                            if possible_matches == "([])" or \
                                    not bin(super_sets)[2:].find("0"):

                                # Then set possible matches to .(all)
                                possible_matches = "(.)"
                            
                            # Add infinite number of matches to accept
                            possible_matches += "*"

                            # Add to final regex
                            regex += possible_matches

                        # Increment count by one less than matched characters
                        i = rng[1] - 1
                        
                        # Break out of loop
                        break    

            # Increment count by one
            i += 1

        # Return final regex
        return regex

    @staticmethod
    def find_super_set(substring):
        """Find super set for given input substring"""

        # Define super sets
        alphabets = "abcdefghijklmnopqrstuvwxyz"
        alphabets_upper = alphabets.upper()

        numbers = "0123456789"

        # Define variable to store find results
        res_bin = 0

        # Check if any character in sub string is persent in 
        # Either of the super sets
        for char in substring:

            # Check of superset alphabets
            if char in alphabets:

                # Set in alphabets bit to True
                res_bin |= 1

            # Check of superset alphabets
            if char in alphabets_upper:

                # Set in alphabets upper bit to True
                res_bin |= 2

            # Check of superset numbers
            if char in numbers:

                # Set in numbers bit to True
                res_bin |= 4

            # Check of superset whitespace space(' ')
            if char == " ":

                # Set has space bit to True
                res_bin |= 8

            # Check of superset signs (ie. !@#$%^&*(){}[]|\:;"'<>?,./~`)
            if char in SIGNS:

                # Set in signs bit to True
                res_bin |= 16

        # Return binary result
        return res_bin


if __name__ == "__main__":
    inputs = [
        (['System.out.println("Hello World")', 'System.out.println("Second Example")'],
         ['print("Hello World")', 'print("Second Example")']),
        (['System.out.println(x)', 'System.out.println(y)'], ['print(x)', 'print(y)']),
        (['System.out.println(x + " " + y)', 'System.out.println(word + " " + number)'],
         ['print(x, y)', 'print(word, number)']),
        (['System.out.println(x.toString() + y.toString())',
          'System.out.println(array_1_str + array_2_str)'],
         ['print(x + y)', 'print(array_1_str + array_2_str)'])
    ]
    for a, b in inputs:
        r_gen = RegexGen(a, b)
        print("{:<70}  {}".format(r_gen.regex_from, r_gen.regex_to))
