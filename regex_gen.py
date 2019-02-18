import re
import sys
from database import DataBase

SIGNS = "!@#$%^&*()_+-={}[]|\\:;\"'<>?,./~`"
ESCAPE_CHARS = "+*?^$\.[]{}()|/"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"
SUPER_CLASSES = ["0-9", "a-z", "A-Z"]
SUPER_SET = NUMBERS + LETTERS + LETTERS.upper()


class RegexGen:

    db_files = {"python": "py_conv_db.db", "java": "java_conv_db.db"}
    match_dict = {}
    diff_dict = {}
    escape_chars = ["+", "(", ")", "\\"]
    cols = 0
    offset = 0
    sl_one_offset = None

    def __init__(self, ln_from, ln_to, lang_from, lang_to):
        """INIT method of RegexGen class"""

        # Store function parameters as class attributes
        # print(self.create_new_regex('print("Hello World 101")', 'print("")'))
        # return

        self.lang_from = lang_from
        self.lang_to   = lang_to
        self.langs = [lang_from, lang_to]
        self.input_lines = [ln_from, ln_to]

        # Initiate database connection
        self.db = db = DataBase(self.langs)
        
        # Find the objective specific code (Similarities between code in 
        # 'from line' and 'to line')
        len_from, len_to = len(ln_from), len(ln_to)
        self.OSC = self.LCS(ln_from, ln_to).strip()

        # Find language specific code for current conversion
        LSC = []
        # LSC.append("".join([char for char in ln_from if char not in self.OSC]))
        # LSC.append("".join([char for char in ln_to if char not in self.OSC]))
        LSC.append(self.get_diff(self.OSC, ln_from))
        LSC.append(self.get_diff(self.OSC, ln_to))
        self.LSC = LSC
        
        print("Objective Specific Code:", self.OSC)
        print("Language Specific Code - from, to:", self.LSC)

        # Get previously maped regex
        # prev_regex, re_id, prev_data = self.match_regex(ln_from)
        # print("Previous Regex: '" + prev_regex + "'")
        # print("prev_data_list: " + str(prev_data))
        # print("Regex ID", re_id)

        # Save LCS of the current and prevoius language specific codes
        # for line in self.get_data():
            
        # with open("regex_gen_data.db") as file:
        #     file.seek(0)
        #     lns = file.readlines()
        #     ln = lns[0].split(" , ")
        #     cols = [i - 1 for i, v in enumerate(ln) if v in self.langs]
        #     total_cols = len(ln) - 1
        #     print("cols", cols)
        #     lns = [ln.split(" , ") for ln in lns]
            
        # if "" not in prev_data:
        #     with open("regex_gen_data.db", "w+") as file:
        #         for i, ln in enumerate(lns):
        #             if ln[0] == re_id:

        #                 # Find LSC strings between previous and current LSCs
        #                 ln.pop(0)
        #                 ln_from, ln_to = self.input_lines
        #                 LSC_from = self.combine(ln_from, prev_data[0])
        #                 LSC_to   = self.combine(ln_to, prev_data[1])

        #                 # If LSC, of either language terminates to null, then
        #                 # input is similar or is a duplicate, hence don't modify
        #                 print("LSC", LSC_from, LSC_to)
        #                 if "" not in [LSC_from, LSC_to]:
        #                     # Escape commas
        #                     LSC = [LSC_from, LSC_to]
        #                     LSC_from.replace(",", "\\,")
        #                     LSC_to.replace(",", "\\,")
        #                     ln_from.replace(",", "\\,")
        #                     ln_to.replace(",", "\\,")
        #                     
        #                     # Increment change resistance
        #                     # if not all([d in "0123456789." for d in prev_data[0][1]]):
        #                     #     prev_data[0][1] = "0"
        #                     # else:
        #                     #     res = float(prev_data[0][1])
        #                     #     prev_data[0][1] = str(res + (100 - res)/7)
        #                     # if not all([d in "0123456789." for d in prev_data[1][1]]):
        #                     #     prev_data[1][1] = "0"
        #                     # else:
        #                     #     res = float(prev_data[1][1])
        #                     #     prev_data[1][1] = str(res + (100 - res)/7)

        #                     # Replace old LSCs and save them to file
        #                     ln[cols[0]] = LSC_from
        #                     ln[cols[1]] = LSC_to
        #                 lns[i] = [re_id] + ln
        #             file.writelines(" , ".join(lns[i]))
        #             file.write("\n")
        # else:
        
        # Add all to and from lines into regex gen database
        # with open("regex_gen_data.db", "a") as file:

        # LSC_0, LSC_1 = LSC[0], LSC[1]
        # print("LSC", LSC)
        # LSC_0.replace(",", "\\,")
        # LSC_1.replace(",", "\\,")

        # Get regex sl number id
        # if re_id:
        #     re_id_next = re_id
        # else:
        #     re_id_next = str(prev_data[0])

        # Escape commas
        data_list = []
        data = ""
        for heading in db.headings:
            for ln, lang in [(ln_from, lang_from), (ln_to, lang_to)]:
                if heading == lang:
                    data_list.append(ln)

        # Find lines in database which can be condensed to a single line
        # The condensed line must statisfy both the input lines but no other
        # lines
        cols = db.cols
        re_id = None
        tmp = []
        for ln in data_list:
            tmp += ["".join(["\\" + c if c in ESCAPE_CHARS else c for c in ln])]
        data_list = tmp
        print("data_list", data_list)
        is_compressable = self.compressable(data_list)
        i = 0
        for ln in db.read():
            if [ln[cols[0]], ln[cols[1]]] != data_list:

                if is_compressable([ln[cols[0]], ln[cols[1]]]):
                    
                    # Generate regex and break, current line can match with one
                    # line at max as all other lines are proven to be
                    # unmatchable amongst themselves
                    data_list = self.combine(data_list, ln, cols)
                    print("REGEX:", data_list)
                    if data_list:
                        re_id = ln[0]
                        data = db.make_data_str(data_list, re_id)
                    break

        # If data string has not be formed, add the data from data_list to file
        if not data:
            data = db.make_data_str(data_list, db.total_rows + 1)

        # Write data to file
        db.write(data, sl_no=re_id, mode=re_id)

    def compressable(self, curr_ln):
        """Return compressability checking function"""

        def is_compressable(ln):
            """Check if a given 2 lines are mapping to the same function and
            hence determine if they are compressable"""

            # Get the shortest form of the lines possible
            ln[0] = self.handle_group_regex(ln[0], max_length=False)
            ln[1] = self.handle_group_regex(ln[1], max_length=False)

            # Get LSC of the 2 lines
            L0 = self.get_diff(curr_ln[0], curr_ln[1])
            L1 = self.get_diff(ln[0], ln[1])

            # Find the LCS of the LSCs
            LCS = self.LCS(L0, L1)
            
            # Remove parts in LSC which are suspected to be OSC
            LSC = [L0, L1]
            for x in range(len(LSC)):
                i = 0
                obj_str = ""
                for char in LCS:
                    find_res = LSC[x].find(char, i)
                    if obj_str:
                        
                        # If a string which is not common to the 2 examples
                        # repeat then it is highly probable that it is LSC if it
                        # is repeated twice as it is common the the 2
                        # conversions of the same example
                        if LSC[x].find(obj_str, i) != -1:
                            LSC[x] = LSC[x].replace(obj_str, "")
                    
                    # Store any mismatches with LCS
                    if find_res - i != 0:
                        obj_str = LSC[x][i:find_res]
                        i = find_res + 1
                    else:
                        i += 1
            
            print("R", LSC[0], LSC[1], LCS, sep=" - ")
            return LSC[0] == LSC[1]

        return is_compressable

    def combine(self, data_list, db_ln, cols):
        """Combine current line and previous line to form a new regex"""
        
        regexes = []
        for i in range(2):

            # Replace with LCS of the 2 examples from the same language
            LCS_str_a = self.handle_group_regex(data_list[i])
            LCS_str_b = self.handle_group_regex(db_ln[cols[i]])
            LCS = self.LCS(LCS_str_a, LCS_str_b)
            print("DL", data_list[i], LCS_str_a)
            print("DL", db_ln[cols[i]], LCS_str_b)
            print("LCS", LCS)

            # Create a merged string of the 2 examples
            merged_str = self.merge_str(data_list[i], db_ln[cols[i]], LCS)
            print("MS1", merged_str)

            # Create regex
            merged_str = self.handle_group_regex(merged_str, max_length=True)
            print("MS2", merged_str)
            regex = self.create_regex(merged_str, LCS)
            regexes.append(regex)

        return regexes

    def handle_group_regex(self, string, max_length=False, sep=False):
        """Replace all group regexes with a representation of the group"""

        res = ""
        in_group = False
        super_cls = ""
        super_cls_list = []

        # Replace super classes in string with the 2 characters of the group
        # with represent the group
        for i, char in enumerate(string):
            if not in_group and super_cls:
                if sep:
                    super_cls_list.append(super_cls + char)
                else:
                    repeatablity = char
                    if max_length:  
                        if re.match(r"\^.", super_cls):
                            super_cls = "".join(SUPER_CLASSES)
                        for cls in SUPER_CLASSES:
                            super_cls = super_cls.replace(cls, cls[0] + cls[-1])
                        res += super_cls
                super_cls = ""
            elif char == "[" and (string[i-1] != "\\" or string[i-2] == "\\"):
                in_group = True
            elif char == "]" and (string[i-1] != "\\" or string[i-2] == "\\"):
                in_group = False
            elif in_group:
                super_cls += char
            else:
                res += char
        return (res, super_cls_list) if sep else res

    def merge_str(self, str_a, str_b, LCS=""):
        """Merge strings a and b according to LCS"""

        print("PARAMS OF MERGE", " - ".join([str_a, str_b, LCS]))
        merged_str = ""
        i = j = k = 0
        z = 0
        
        def merge_two_strs(str_x, str_y):
            """Merges any two given strings"""
            
            # Store the groups seperately and don't include them in merging
            # process
            str_x, temp = self.handle_group_regex(str_x, sep=True)
            res_str = "".join(["[" + x[:-1] + "]" + x[-1] for x in temp])
            str_y, temp = self.handle_group_regex(str_y, sep=True)
            res_str = "".join(["[" + x[:-1] + "]" + x[-1] for x in temp])
            print("T", res_str)
            y = 0
            for char in str_x:
                x = str_y.find(char, y)
                
                # If character not in string B, then add it to merged string
                if x == -1:
                    res_str += char
                    
                # Else add all characters of string B till next match
                else:
                    res_str += str_y[y:x+1]
                    y = x+1

            # Add any excess of sub string b to merged string
            res_str += str_y[y:]
            return res_str
        
        # If LCS is not given, just add them without it
        if not LCS:
            return merge_two_strs(str_a, str_b)

        str_a_finder = self.find_next(str_a)
        str_b_finder = self.find_next(str_b)

        while k < len(LCS):
            
            # If next characters of all three strings match add to merged string
            str_a_find = str_a_finder(LCS[k], i)
            str_b_find = str_b_finder(LCS[k], j)
            if str_a_find - i == 0 and str_b_find - j == 0:
                merged_str += LCS[k]
                i += 1
                j += 1
                k += 1
            else:
                
                # Create substrings of portions of string in focus
                sub_str_a = str_a[i:str_a_find]
                sub_str_b = str_b[j:str_b_find]
                merged_str += merge_two_strs(sub_str_a, sub_str_b)

                # Update i and j index values to final values
                i = str_a_find
                j = str_b_find
            
        return merged_str

    def find_next(self, string):
        """Return find function"""

        def find(char, start):
            """Find next matching character"""

            i = start
            in_group = False

            # Lambda functions to check if open square brackets are escaped
            cond_one = lambda i: (i == 1 and string[i-1] != "\\")
            cond_two = lambda i: (i > 1 and (string[i-1] != "\\"
                                  or string[i-2] == "\\"))
            for c in string[start:]:
                
                # Return character index if not in group
                if c == char and not in_group:
                    return i
                if c == "[":
                    if i == 0 or cond_one(i) or cond_two(i):
                        in_group = True
                if c == "]":
                    if i == 0 or cond_one(i) or cond_two(i):
                        in_group = False
                i += 1
        return find
            

    def unescape_str(self, string):
        """Unescape the given input string"""
        
        # If any escaped character is found unescape it
        res = ""
        for i, char in enumerate(string[:-1]):
            if not(char == "\\" and string[i+1] in ESCAPE_CHARS):
                res += char
        return res + string[-1]

    def create_regex(self, string, LSC):
        """Create new regex string for given LSC"""

        # Unescape both strings
        string = self.unescape_str(string)
        LSC    = self.unescape_str(LSC)

        # Create LSC for current input string
        # Iterate over characters in the input string
        print("CREATE_REGEX", string, LSC)
        re_expr = ""
        temp = ""
        i = 0
        j = 0

        while j < len(LSC):
            
            # Check if character is present in merged string
            char = "\\" + LSC[j] if LSC[j] in ESCAPE_CHARS else LSC[j]
            if string.find(LSC[j], i) - i == 0:
                
                # If temp is not empty get super class of temp string and add it
                if temp:
                    re_expr += self.str_super_cls(temp, char)
                    temp = ""

                # Append character to regex expression
                re_expr += char
                j += 1

            else:
                temp += string[i]
            i += 1

        # If temp string is not empry, add rest to regex expression
        if temp:
            re_expr += self.str_super_cls(temp, "")

        # Return regex_expression
        return re_expr

    def str_super_cls(self, string, LSC_next, repeatablity=0):
        """Find super class for the given input string"""

        # Based on repeatability, set the acceptable number of times a
        # character can occur
        repeat_char = "*"
        # if type(repeatablity) == int:
        if repeatablity < 0:
            repeat_char = "?"
        elif repeatablity > 0:
            repeat_char = "+"
        # elif type(repeatablity) in [list, tuple]:
        #     if len(repeatablity) == 1:
        #         repeat_char = "{" + repeatablity[0] + "}"
        #     elif len(repeatablity) == 2:
        #         repeat_char = "{{{l[0]}, {l[1]}}}".format(l = repeatablity)
        
        # Find super class of given string
        str_super_cls = "["
        if any([num in string for num in NUMBERS]):
            str_super_cls += SUPER_CLASSES[0]
        if any([ll in string for ll in LETTERS]):
            str_super_cls += SUPER_CLASSES[1]
        if any([ul in string for ul in LETTERS.upper()]):
            str_super_cls += SUPER_CLASSES[2]
        used_chars = ""
        for char in string:
            if char not in SUPER_SET and char not in used_chars:
                str_super_cls += char
                used_chars += char

        # Escape required characters
        super_cls_escaped = ""
        for char in str_super_cls[1:]:
            if char in ESCAPE_CHARS:
                super_cls_escaped += "\\" + char
            else:
                super_cls_escaped += char
        super_cls_escaped = "[" + super_cls_escaped

        # If string contains all the super classes, replace it with a not
        # condition with character, set to next LSC character
        if all(cls in super_cls_escaped for cls in SUPER_CLASSES):
            if LSC_next:
                super_cls_escaped = "[^" + LSC_next
            else:
                super_cls_escaped = "."

        # Add close bracket if there is a matching open bracket
        if super_cls_escaped[0] == "[":
            super_cls_escaped += "]"
                
        # Concatinate allowed number of repeats character with str_super_cls
        return super_cls_escaped + repeat_char


    def get_diff(self, str_a, str_b):
        """Get Object Specific code for given string"""

        diff = ""
        j, i = 0, 0

        # Set longer string as str_a and shorter as str_b
        if len(str_b) > len(str_a):
            temp = str_a
            str_a = str_b
            str_b = temp

        # For each character in the shorter string, check if it is present in
        # longer string. If not add it to differences string
        for char in str_b:
            i = str_a.find(char, j)
            if i == -1:
                diff += char
                j += 1
            else:
                diff += str_a[j: i]
                j = i + 1
        
        # Add rest of the untouched string to the differences string
        diff += str_a[j:]
        return diff
        

    def LCS(self, str_a, str_b):
        """Define a handler of the LCS_recursive function"""

        # Store lengths of strings
        len_a, len_b = len(str_a), len(str_b)

        def LCS_rec(ia, ib, memory):
            """Get the longest chain of common words between the 2 given strings"""

            # If index out of bounds, return function
            if ia == len_a or ib == len_b:
                return ""

            # Check if substrings are already computed and stored
            # If yes, return it
            if memory[ia][ib] != 0:
                return memory[ia][ib]

            # Check if characters are equal, append to final string and compute
            # next character, add it to memory and return it
            if str_a[ia] == str_b[ib]:
                memory[ia][ib] = str_a[ia] + LCS_rec(ia + 1, ib + 1, memory)
                return memory[ia][ib]

            # Else compute both the other possibilities
            result_a = LCS_rec(ia + 1, ib, memory)
            result_b = LCS_rec(ia, ib + 1, memory)

            # Store and return longest string
            if len(result_a) > len(result_b):
                memory[ia][ib] = result_a
            else:
                memory[ia][ib] = result_b
            return memory[ia][ib]

        return LCS_rec(0, 0, [[0 for _ in range(len_b)] for _ in range(len_a)])

    
    def match_regex(self, line):
        """Return a regex that matches the input line"""

        # Check if a regex map exists for given line
        # Open regex convertion database
        with open(self.db_files[self.lang_from]) as file:

            # Read each line in file
            for re_expr in file.readlines():

                # Get regex expression from line
                re_id, re_expr = re_expr.split(" ", 1)
                re_expr = re.sub(r"\[\$[0-9]\]", "",
                                    re_expr).strip()
                print("REP", re_expr)

                # Search of match between line and expression
                if re.search(re_expr, line):
                    
                    # Get regex_gen data
                    with open("regex_gen_data.db") as file:

                        # Split line at comma
                        ln = [ln.strip() for ln in file.readline().split(" , ")]
                        db_lns = [ln]

                        # Get data
                        cols = self.db.cols
                        lns = [ln.strip("\n").split(" , ") for ln in file.readlines()]
                        db_lns += lns

                        # Else get previous data from line
                        print("cols", cols)
                        print("LNS", lns)
                        data = []
                        if lns:
                            data = [ln[1:] for ln in lns if ln[0] == re_id][0]
                        
                        # If line is not found get last regex id, quit loop
                        if not data:
                            re_id_next = max([ln[0] for ln in lns] + [1])
                            return re_expr, re_id, [re_id_next, None]

                        print("data", data)
                        data = [data[cols[0]+1].strip(),data[cols[1]+1].strip()]
                    
                    # If found, return it
                    return re_expr, re_id, data

                # Return only the regex_expression whick is matched
                return re_expr, None, ["", ""]
        return None, None, ["", ""]

    def __del__(self):
        """Destructor method of RegexGen class"""
        
        # Close database
        # self.db.close()
        pass


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
    #for a, b in inputs:
    #    r_gen = RegexGen(a, b)
    #    print("{:<70}  {}".format(r_gen.regex_from, r_gen.regex_to))
    # res = RegexGen('print("Hello World")', 'System.out.println("Hello World")', "python", "java")
    # res = RegexGen('print("Hello!")', 'System.out.println("Hello!")', "python", "java")
    # res = RegexGen('print("auto end return")', 'System.out.printf("auto end return\\n")', "python", "java")
    # res = RegexGen('print("Hello World 2")', 'System.out.println("Hello World 2")', "python", "java")
    # res = RegexGen('print("ABCD")', 'System.out.println("ABCD")', "python", "java")
    # res = RegexGen('print("Hello World Testing")', 'System.out.println("Hello World Testing")', "python", "java")
    # res = RegexGen('print(str(1) + str(2))', 'System.out.println(Integer.toString(1) + Integer.toString(2))', "python", "java")
    # res = RegexGen('math.sqrt(4)', 'Math.sqrt(4)', "python", "java")
    # res = RegexGen('print("Hello", end="\\n\\n")', 'System.out.println("Hello\\n\\n")', "python", "java")
    # res = RegexGen('print("HI", end="!\\n")', 'System.out.println("HI!\\n")', "python", "java")
    # res = RegexGen('print("Good Bye", end="!\\n")', 'System.out.println("Good Bye")', "python", "java")
    # res = RegexGen('print("3.14 ", end="This is the value of pi\\n")', 'System.out.println("3.14 This is the value of pi")', "python", "java")
    res = RegexGen('print("Hours in day = ", end="24hrs - time wasted\\n")', 'System.out.println("Hours in day = 24hrs - time wasted")', "python", "java")
    

