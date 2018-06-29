"""Process code and act as input to conversion classes"""
import re

from language import Language
from languages.java import Java
from languages.python import Python
from languages.cpp import CPP
from languages.c import C

PY_CONV_DB = "py_conv_db.db"
JAVA_CONV_DB = "java_conv_db.db"
CPP_CONV_DB = "cpp_conv_db.db"
C_CONV_DB = "c_conv_db.db"


class CodeProcessor:
    lang_cls = {"python": Python, "java": Java, "cpp": CPP, "c": C}
    conv_dbs_ptr = {"python": PY_CONV_DB, "java": JAVA_CONV_DB,
                    "cpp": CPP_CONV_DB, "c": C_CONV_DB}
    conv_db = []
    file_lines = []
    file_str = None
    end_app_list = []
    curr_level = 0
    multi_statement = -1
    indent_base = -1
    char_diff = 0

    def __init__(self, file_path, lang_from, lang_to, outfile_path):
        """Initializes code processor class"""

        # Store input parameters into class attributes
        self.file_path = file_path
        self.outfile_path = outfile_path

        # Store from and to languages
        self.lang_from = lang_from
        self.lang_to = lang_to

        # Initialize from and to language conversion classes
        from_cls = self.lang_cls[lang_from]()
        to_cls = self.lang_cls[lang_to](outfile_path)

        # Store all class funcs in list
        lang_rec_funcs = ["get_language", "recognize", "validate"]
        self.funcs = [item for item in dir(Language) if
                      not (item.startswith("__") or item in lang_rec_funcs)]

        # Make list to store all recognition functions
        self.rec_funcs = [fn for fn in self.funcs if fn[:2] == "is"]

        # Make a list to store all from conversion functions
        from_conv_funcs = [fn for fn in self.funcs if fn.startswith("get")]
        self.from_conv_funcs = [from_cls.__getattribute__(fn)
                                for fn in from_conv_funcs]
        to_conv_funcs = [fn for fn in self.funcs if fn.startswith("convert")]
        self.to_conv_funcs = [to_cls.__getattribute__(fn)
                              for fn in to_conv_funcs]

        # Map recognition and conversion functions
        conv_funcs = zip(self.from_conv_funcs, self.to_conv_funcs)
        zipped_funcs = zip(self.rec_funcs, conv_funcs)
        self.funcs_map = {rec_fn: conv_fn for rec_fn, conv_fn in zipped_funcs}

        # Convert string names to function pointers
        self.funcs = [from_cls.__getattribute__(fn) for fn in self.funcs]
        self.rec_funcs = [from_cls.__getattribute__(fn)
                          for fn in self.rec_funcs]

        # Store language classes as attributes
        self.from_cls = from_cls
        self.to_cls = to_cls

        # Read conversion database
        self.read_conv_db()

        # Save preferred indentation base
        self.to_indent_preference = self.to_cls.preferred_indent_base

        # Declare list to store all variables name if language is python
        self.vars = []

    @staticmethod
    def indent(line):
        """Returns indentation level of line"""

        # Check if line is just whitespace
        if not line.strip():
            # If yes, return 0
            return 0

        # Return indentation level of line
        return len(line) - len(line.lstrip())

    def convert(self):
        """Starts conversion of file from language a to language b"""

        # Store file into local variable
        file_path = self.file_path

        # Open file for reading
        with open(file_path) as fptr:

            # Gets all lines in file as a list
            lines = fptr.readlines()

            # Get indentation base of the file
            self.indent_base = self.get_indent_base(lines)

            # Iterate over lines in file
            i = 0
            while i < len(lines):

                # Declare variable to store conversion
                conv_line = None

                # Recognize line
                line_type, x = self.recognize(lines, i)

                # If is line is recognized as a built in function
                # Run corresponding conversion function
                if line_type == "built-in definition":
                    func = x
                    params = self.funcs_map[func][0](lines, i)

                    # Check if line is required to be omitted
                    if params[0] == "omit":
                        # Skip requested number of lines
                        i += params[1]
                        continue

                    # Convert line to language B
                    conv_line = self.funcs_map[func][1](*params[:-2])

                    # If start or end of line specified, add to lines
                    if params[-2]:
                        conv_line = (conv_line[0] + params[-2], conv_line[1])

                        # Multiple statements are executed set flag to true
                        self.multi_statement = 0

                    if params[-1]:
                        conv_line = (conv_line[0], conv_line[1] + params[-1])

                # If no conversion failed, set conversion line to input line
                if not conv_line:
                    conv_line = tuple([[lines[i].rstrip("\n")]])

                # Log the converted line
                self.write_to_file(lines, i, *conv_line)

                # Increment count
                i += 1

            # Check if last line(s) are empty
            empty_lns_count = 0
            if not self.file_lines[-1].strip():
                empty_lns_count = 1
                while True:
                    
                    # Check if previous line is empty
                    if not self.file_lines[-empty_lns_count - 1].strip():

                        # If yes, increment count(to previous line)
                        empty_lns_count += 1
                        continue
                    
                    # Else break out of loop
                    break
            
            # Remove empty lines from file
            if empty_lns_count:
                self.file_lines = self.file_lines[:-empty_lns_count]

            # Add all remaining endings to file
            self.add_endings(self.curr_level, self.curr_level)

            # Check lang x to python conversion
            if self.lang_to == "python":

                # Add main function call
                self.file_lines += [
                    "",
                    "",
                    "if __name__ == \"__main__\":",
                    "    {}().main()".format(
                        self.outfile_path.split(".")[0].title())]

            # Convert file lines list to file string
            self.file_str = "\n".join(self.file_lines) + "\n" * empty_lns_count

            # Try to match regex expression
            for match in self.match_regex():
                # Get start and end of regex match
                start = match[1].start() + self.char_diff
                end = match[1].end() + self.char_diff

                # If a regex match is found, run regex substitute function
                sub = self.regex_substitute(*match, self.file_str[start:end])

                # Record file length to calculate character difference
                # Due to substitution
                prev_len = len(self.file_str)
                self.file_str = self.file_str[:start] + sub + self.file_str[end:]

                # Increase store difference to match future conversions
                self.char_diff += len(self.file_str) - prev_len

            # Convert file back to lines
            self.file_lines = self.file_str.split("\n")

    def regex_substitute(self, regex_from, regex_obj, regex_to, regex_str):
        """Converts line from regex form from to regex form to"""

        # Replace all groups with numbers
        regex_to_str = self.replace_group_no(regex_to, 1)

        # Check if line is a variable declaration in python
        if self.lang_from == "python" and "=" in regex_from:

            # Then get variable name
            var_name = regex_obj.group(1).split("=")[0].rstrip("+-*/").strip()

            # Check if variable name exists in already declared variables
            if var_name in self.vars:
                # Then break out of method
                return regex_str

            # Else add variable name to list
            self.vars.append(var_name)

        # Substitute and return regex pattern from language A to B
        return re.sub(regex_from, regex_to_str, regex_str)

    def replace_group_no(self, regex_str, group_no):
        """Replaces groups in regex string with index of group number"""

        # Declare variables to store start and end of group
        start = -1

        # Check if required to omit next ')', and initialize delete to false(-1)
        omit_count = 0
        delete = -1

        # Iterate through all characters in to_regex string
        for i, char in enumerate(regex_str):

            # Check if start of group
            if char == "(" and regex_str[i - 1] != "\\":
                
                # Check if group is negative lookbehind
                if regex_str[i+1:i+4] == "?<!":

                    # If yes continue loop, and set delete group to true
                    omit_count += 1
                    delete = i
                    continue

                # Then store start index
                start = i

            # Check if end of group
            elif char == ")" and regex_str[i - 1] != "\\":

                # If under omit, decrease count by one
                if omit_count:
                    omit_count -= 1

                    # If delete, strip till current character(inclusive)
                    if delete != -1:

                        # Remove string till current character
                        return self.replace_group_no(regex_str[:delete] + regex_str[i+1:], group_no)
                        
                    continue

                # Then replace with group number
                regex_str = regex_str[:start] + "\\" \
                            + str(group_no) + regex_str[i + 1:]

                # Call recursively
                return self.replace_group_no(regex_str, group_no + 1)

        # If no groups were found, return input regex string
        return regex_str

    def write_to_file(self, fptr, i, lines, end=None):
        """Modify and write lines to file in memory"""

        # Get current level of line
        curr_level = self.curr_level

        # Check if line(s) is the end of definition
        level_decrement = (self.is_def_end(fptr, i) if self.lang_to != "python"
                           else fptr[i].count("}"))

        # Check if is a multiline statement
        if self.multi_statement == 1:
            level_decrement = 1
            self.multi_statement = -1

        # Set act on multiline statement to true
        if self.multi_statement == 0:
            self.multi_statement = 1

        # Check for level decrement
        if level_decrement:

            # Add appropriate endings
            curr_level = self.add_endings(level_decrement, curr_level)

            # If conversion is to python code, then decrease
            # Current level based on level decrement
            if self.lang_to == "python":

                curr_level -= level_decrement

                # Remove end bracket from line
                for j in range(level_decrement):
                    lines[-j -1] = lines[-j -1].rstrip("}")

        # Set indent search file 
        indent_search_fptr = "fptr" if self.lang_to == "python" else "curr_line"

        # Append current line to file
        for line in lines:

            # Calculate number of spaces for indentation
            indentation = " " * (curr_level * self.to_indent_preference)

            # Add Semicolon if required
            line = line.lstrip()
            if self.lang_to != "python":
                if line:
                    semicolon_req = (not self.from_cls.has_semicolon
                                    and line[-1] not in ["{", "}"])
                    line = line.rstrip() + ";" if semicolon_req else line

            # Check if language is python
            if self.lang_to == "python":

                # Then remove all trailing semi-colons
                line = line.split("//")[0].split("/*")[0].rstrip().rstrip(";")

            # Append line to file
            line = indentation + line
            self.file_lines.append(line)

            # If open brackets found in line, increment current level
            if "{" in (fptr[i] if indent_search_fptr == "fptr" else line):
                curr_level += 1

        # Store line to be added to end of definition
        if end:
            self.end_app_list.append(end)

        # Update global variable
        self.curr_level = curr_level

    def add_endings(self, level_decrement, curr_level):
        """Add appropriate ending lines to file"""

        # Add endings from end append attribute to file
        for _ in range(level_decrement):

            # Check if end append list is empty
            if not self.end_app_list:
                # If yes, continue loop
                break

            # Iterate through lines in end append list
            for end_line in self.end_app_list.pop():

                # Check if line is a close bracket
                if "}" in end_line:
                    curr_level -= 1
                if "{" in end_line:
                    curr_level += 1

                # Calculate number of spaces for indentation
                indentation = " " * (curr_level * self.to_indent_preference)

                # Modify line
                mod_line = indentation + end_line.lstrip()

                # Pop and add line to file
                self.file_lines.append(mod_line)

        # Return updated current level value
        return curr_level

    def is_def_end(self, fptr, i):
        """Checks if the current line is the last line of the definition"""

        # Check if is first line of file or line is a blank line
        if i == 0 or fptr[i].strip() == "":
            
            # Return difference in level to be 0
            return 0

        # Get indentation of current line
        prev_level = self.indent(fptr[i - 1]) // self.indent_base
        curr_level = self.indent(fptr[i]) // self.indent_base

        # Return difference if positive
        diff = prev_level - curr_level
        return 0 if diff < 0 else diff

    def get_indent_base(self, fptr):
        """Gets the indentation base(factor) of input file"""

        # Store the difference of indentation
        diff = 0

        # Declare variable to store line number
        i = 0

        # While not difference
        while not diff and i != len(fptr):
            # Calculate the difference in indentation
            diff = self.indent(fptr[i])

            # Increment line count
            i += 1

        # Return difference in indentation
        return diff if diff else self.to_cls.preferred_indent_base

    def recognize(self, fptr, i):
        """Recognize line and segregate into categories"""

        # Run recognition functions to recognize line
        for func in self.rec_funcs:

            # Run recognition function
            if func(fptr, i):
                # Return function name with function type on success
                return "built-in definition", func.__name__

        # If match not found return none
        return None, None

    def match_regex(self):
        """Match input file with regex expressions"""

        # Iterate over regex expressions
        for expr in [record[0] for record in self.conv_db]:

            # Compile regex
            expr_complied = re.compile(expr[-1])

            # Reset character difference as self.file_str is updated
            self.char_diff = 0

            # Check if pattern matches
            for match in expr_complied.finditer(self.file_str):
                # If expression matches, return corresponding to conversion
                regex_ln = [ln[1] for ln in self.conv_db if ln[1][0] == expr[0]]
                yield expr[-1], match, regex_ln[0][-1]

    def read_conv_db(self):
        """Read data from conversion database"""

        # Declare variable to store conversion database
        conv_db = []

        # Open appropriate conv_dbs_ptr
        for db in [self.conv_dbs_ptr[self.lang_from], self.conv_dbs_ptr[self.lang_to]]:
            # Open conversion database
            with open(db) as fptr:
                # Read file
                lines = fptr.readlines()

                # Store in database
                conv_db.append([line.strip("\n").split(" ", 1) for line in lines])

        # Merge file lines and stores as class attribute
        self.conv_db = list(zip(conv_db[0], conv_db[1]))

    def write_file_to_disk(self):
        """Writes converted file from memory to disk"""

        # Get output file name
        file_path = self.to_cls.outfile_path

        try:
            # Check if file exists
            with open(file_path, "x"):

                # Set file write permission to True
                write = "y"

        except (FileExistsError, Exception) as err:

            # Check if is FileExistsError
            if err.errno == 17:

                # If yes, prompt for overwrite permission
                print("File {} exists".format(file_path))
                write = input("Overwrite? <Y/N> ").lower()

                # Request valid input if input is invalid
                while write not in ["y", "n"]:
                    write = input("Please input only 'Y' or 'N' ").lower()

            else:

                # Else return error
                print("File write FAILED")
                return err

        if write == "y":
            # Overwrite if permission is granted
            with open(file_path, "w") as fptr:
                # Write lines from memory to disk
                fptr.writelines("\n".join(self.file_lines))
                print("File Write SUCCESSFUL")
                print("Output:", file_path)

        else:
            # Else permission is denied
            print("File write permission DENIED")


if __name__ == "__main__":
    # file = "outfile.java"
    # outfile_path = "outfile.py"
    # processor = CodeProcessor(file, "java", "python", outfile_path)
    file = "test_examples/python_file_1.py"
    outfile_path = "outfile.java"
    processor = CodeProcessor(file, "python", "java", outfile_path)
    processor.convert()
    error = processor.write_file_to_disk()
