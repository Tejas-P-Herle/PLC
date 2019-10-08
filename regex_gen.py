#!/usr/bin/env python3

import re
import sys
import difflib
from database import DataBase

SIGNS = "!@#$%^&*()_+-={}[]|\\:;\"'<>?,./~`"
ESCAPE_CHARS = "+*?^$\.[]{}()|/"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"
SUPER_CLASSES = ["0-9", "a-z", "A-Z"]
SUPER_SET = NUMBERS + LETTERS + LETTERS.upper()


class RegexGen:

    db_files = {"python": "py_conv_db.db", "java": "java_conv_db.db",
                "cpp": "cpp_conv_db.db", "c": "c_conv_db.db"}
    match_dict = {}
    diff_dict = {}
    escape_chars = ["+", "(", ")", "\\"]
    cols = 0
    offset = 0
    sl_one_offset = None
    error = 0

    def __init__(self, ln_from, ln_to, lang_from, lang_to):
        """INIT method of RegexGen class"""

        # Group lines and languages
        langs = [lang_from, lang_to]
        input_lns = [ln_from, ln_to]

        # Initiate database connection
        self.db = db = DataBase(langs)
        
        # Find the objective specific code (Similarities between code in 
        # 'from line' and 'to line')
        len_from, len_to = len(ln_from), len(ln_to)
        self.OSC = self.LCS(ln_from, ln_to).strip()

        # Find language specific code for current conversion
        # LSC = []
        # for ln in [ln_from, ln_to]:
        #     temp = []
        #     
        #     # Find difference and store as string
        #     for diff in self.get_diff(self.OSC, ln):
        #         temp.append([char[1] for char in diff])
        #     LSC.append(["".join(lst) for lst in temp])
        # self.LSC = LSC
        
        # print("Objective Specific Code:", self.OSC)
        # print("Language Specific Code - from, to:", self.LSC)

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
                    # Add groups to regex, such as to map input OSC code to 
                    # output OSC code
                    #data_list = ['print\\("[^"]*"\\, end="[^\\\\]*\\\\n[a-z\\\\]*"\\)', 'System\\.out\\.println\\("[^"]*"\\)']
                    #input_lns = ['print("Hello World", end="!\\n")','System.out.println("Hello World!")']
                    data_list = self.map_groups(data_list, input_lns)
                    print("GRP MAP", data_list)
                    if data_list:
                        re_id = ln[0]
                        data = db.make_data_str(data_list, re_id)
                    break

        # If data string has not be formed, add the data from data_list to file
        if not data:
            data = db.make_data_str(data_list, db.total_rows + 1)

        # Write data to file
        db.write(data, sl_no=re_id, mode=re_id)
        db.write_to_conv_db(data, self.db_files)

    def compressable(self, curr_ln):
        """Return compressability checking function"""
        
        def is_compressable(ln):
            """Check if a given 2 lines are mapping to the same function and
            hence determine if they are compressable"""

            # Get the shortest form of the lines possible
            ln[0] = self.handle_group_regex(ln[0], max_length=False)
            ln[1] = self.handle_group_regex(ln[1], max_length=False)

            # Get LSC of the 2 lines
            diff_0 = self.get_diff(curr_ln[0], curr_ln[1])
            diff_1 = self.get_diff(ln[0], ln[1])
            
            # Declare variables to store compressablity status
            is_compressable_flag = True
            diff_sec = 0
            diff_list = [diff_0, diff_1]

            # If addtions and deletions are the same,
            # then the lines are compressable
            # Iterate through insertions and deletions
            while diff_sec < len(diff_0) and is_compressable_flag:
                
                # Check if number of insertions and deletions are the same
                # in both conversions. If not break the loop and set flag False
                if len(diff_0[diff_sec]) != len(diff_1[diff_sec]):
                    is_compressable_flag = False
                    break

                # Else iterate through all the characters in the section
                i = 0
                char_diff = None
                char_diff = diff_0[diff_sec][0][0] - diff_1[diff_sec][0][0]
                while i < len(diff_0[diff_sec]):
                    
                    # Declare variable for easy access
                    diff_0_char = diff_0[diff_sec][i]
                    diff_1_char = diff_1[diff_sec][i]

                    # Check if the characters in the two lists are the same
                    if diff_0_char[1] != diff_1_char[1]:
                        is_compressable_flag = False
                        break

                    # Check continuity of characters
                    if diff_0_char[0] - diff_1_char[0] != char_diff:
                        if diff_0[diff_sec][i] - diff_0[diff_sec][i-1] == 1:
                            is_compressable_flag = False
                            break
                        else:
                            char_diff = diff_0_char[0] - diff_1_char[0]
                    
                    # Increment character index
                    i += 1

                # Increment section
                diff_sec += 1

            # Return compressablity result
            return is_compressable_flag

            # print("L0L1 " + " --- " +  L0 + " --- " + L1)
            #
            # # Find the LCS of the LSCs
            # LCS = self.LCS(L0, L1)
            # 
            # # Remove parts in LSC which are suspected to be OSC
            # LSC = [L0, L1]
            # for x in range(len(LSC)):
            #     i = 0
            #     obj_str = ""
            #     for y, char in enumerate(LCS):
            #         if obj_str:
            #             
            #             # If a string which is not common to the 2 examples
            #             # repeats then it is highly probable that it is LSC if
            #             # it is repeated twice as it is common the the 2
            #             # conversions of the same example
            #             if LSC[x].find(obj_str, i) != -1:
            #                 LSC[x] = LSC[x].replace(obj_str, "")
            #                 obj_str = ""
            #                 i = LSC[x].find(LCS[y], i) 
            #             else:
            #                 i = find_res + 1
            #         find_res = LSC[x].find(char, i)
            #         
            #         # Store any mismatches with LCS
            #         if find_res - i != 0:
            #             obj_str = LSC[x][i:find_res]
            #         else:
            #             i += 1
            # 
            # print("LSC01" + " --- " +  LSC[0] + " --- " + LSC[1])
            # print(LSC[0] == LSC[1])
            # return LSC[0] == LSC[1]

        return is_compressable

    def combine(self, data_list, db_ln, cols):
        """Combine current line and previous line to form a new regex"""
        
        regexes = []
        for i in range(2):

            # Replace with LCS of the 2 examples from the same language
            LCS_str_a = self.handle_group_regex(data_list[i])
            LCS_str_b = self.handle_group_regex(db_ln[cols[i]])
            LCS = self.LCS(LCS_str_a, LCS_str_b)

            # Create a merged string of the 2 examples
            db_ln_re_handled = self.handle_group_regex(db_ln[cols[i]],
                                                       max_length=True)

            merged_str = self.merge_str(data_list[i], db_ln_re_handled, LCS)
            print("MS1", merged_str)

            # Create regex
            merged_str = self.handle_group_regex(merged_str, max_length=True)
            print("MS2", merged_str)
            regex = self.create_regex(merged_str, LCS)
            regexes.append(regex)

        return regexes

    def is_group(self, string, i, check):
        return (check and ((i == 0 or string[i-1] != "\\")
                or (i != 1 and string[i-2] == "\\")))


    def handle_group_regex(self, string, max_length=False, sep=False):
        """Replace all group regexes with a representation of the group"""

        res = ""
        in_group = False
        super_cls = ""
        super_cls_list = []
        in_group_index = False
        omit_bracket = False

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
            elif self.is_group(string, i , char == "["):
                if string[i+1] == "$":
                    in_group_index = True
                    res = res[:-1]
                else:
                    in_group = True
            elif self.is_group(string, i, char == "]"):
                if in_group:
                    in_group = False
                    omit_bracket = True
                else:
                    in_group_index = False
            elif in_group:
                super_cls += char
            elif not in_group_index and not omit_bracket:
                res += char
            else:
                omit_bracket = False
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

        str_a_finder = self.finder(str_a)
        str_b_finder = self.finder(str_b)

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

    def finder(self, string):
        """Return find function"""
        
        def find(str_find, start):
            """Find next matching character or return next index in group"""

            i = 0
            if start:
                i = start
            in_group = False
            start_grp = -1
            length = len(str_find)

            while i < len(string) and i <= len(string) - length:
                
                curr_str = string[i]
                curr_str += "".join([string[i+n+1] for n in range(length-1)])

                # Return character index if not in group
                if curr_str != "" and curr_str == str_find and not in_group:
                    return i
                if (self.is_group(string, i, "[" in curr_str)
                        and string[i+1] != "$"):
                    if not str_find:
                        start_grp = i
                    in_group = True
                if self.is_group(string, i, "]" in curr_str):
                    if not str_find:
                        return start_grp, i
                    in_group = False
                i += 1
        return find
    

    def escape_str(self, string):
        """Escape the given input string"""

        # If any character that belongs to escape set, escape the character
        res = ""
        for char in string:
            if char in ESCAPE_CHARS:
                res += "\\" + char
            else:
                res += char
        return res

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
        
        # Get differences between the strings
        insertions = []
        deletions = []
        print("STRAB", str_a, str_b)
        for i, diff in enumerate(difflib.ndiff(str_a, str_b)):
            if diff[0] == "+":
                insertions.append((i, diff[-1]))
            if diff[0] == "-":
                deletions.append((i, diff[-1]))

        diff = [insertions, deletions]
        return diff
        

    def LCS(self, str_a, str_b):
        """Define a handler of the LCS_rec function"""

        # Store lengths of strings
        len_a, len_b = len(str_a), len(str_b)

        def LCS_rec(ia, ib, memory):
            """Get the longest chain of common
            words between the 2 given strings"""

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

    def map_groups(self, regexes, examples):
        """Adds groups into regex to map input variables to output variables"""

        # Iterate through both the regexes and find differences
        print("MAP", regexes, examples)
        grand_maps = [[], []]

        # Get start and stop indexes for regexes
        # And find example matches for the given regex indexes
        for x in range(len(regexes)):
            i = 0
            j = 0
            start_ex = -1
            start_re, ex_re = -1, -1
            re_finder = self.finder(regexes[x])
            diff = ""
            finding_diff = False
            regex = regexes[x]
            example = self.escape_str(examples[x])
            while i < len(regex) and j < len(example):
                if not finding_diff and diff:
                    grand_maps[x].append([start_re, end_re + 2, diff])
                    diff = ""

                if self.is_group(regex, i, regex[i] == "["):
                    start_re, end_re = re_finder("", i)
                    i = end_re + 2
                    start_ex = j
                    print("SE", start_re, end_re)
                    finding_diff = True

                elif regex[i] == example[j]:
                    i += 1
                    j += 1
                    finding_diff = False
                else:
                    diff += example[j]
                    j += 1

        print("REMPS", grand_maps)
        # Match appropriate regex groups
        group_maps = []
        grand_maps_sorted = [[], []]
        for i, map_ in enumerate(grand_maps):
            grand_maps_sorted[i] += sorted(map_, key=lambda l: len(l[2]),
                                           reverse=True)
        for map_a in grand_maps_sorted[0]:
            for map_b in grand_maps_sorted[1]:
                if map_a[-1] in map_b[-1]:
                    str_a, str_b = map_a[-1], map_b[-1]
                else:
                    str_a, str_b = map_b[-1], map_a[-1]
                is_sub_str = str_b.find(str_a)
                if is_sub_str != -1:
                    map_ = [map_a[:2], map_b[:2]]
                    if map_ not in group_maps:
                        group_maps.append(map_)
                    break
        print("REGRPS", group_maps)
        # Add group numbers in the regex
        return self.insert_groups(group_maps, regexes)

    def insert_groups(self, maps, regexes):
        """Insert group numbers for replacement of regex matches"""

        print("RE", regexes, maps)

        # For both direction, to and from replace indexed ranges with group
        # numbers
        template = "([${}]{})"
        regxs_grpd = []
        for i, regex in enumerate(regexes):
            grp_no = 1
            end = 0
            regx_grpd = ""
            for map_ in maps:
                regx_grpd += (regex[end: map_[i][0]]
                              + template.format(grp_no,
                                                regex[map_[i][0]: map_[i][1]]))
                end = map_[i][1]

                grp_no += 1
            regxs_grpd.append(regx_grpd + regex[end:])
        return regxs_grpd
                    
    def replace_groups(self, ex_a, ex_b, maps_set):
        """Replace appropriate groups with their maps"""
        for map_ in maps_set:
            print("MAP")

    def discover_map(self, ex_a, ex_b_finder):

        # Discover map of conversions for given group
        def find(i, j, end_a):
            maps = []
            ex_a_buffer = ""
            start = -1
            prev_find = None
            find      = None
            for x, char in enumerate(ex_a[i:end_a]):
                find = ex_b_finder(ex_a_buffer+char, j)
                if find != None:
                    prev_find = find
                    if start == -1:
                        start = i + x
                    ex_a_buffer += char
                else:
                    if ex_a_buffer:
                        from_ = (start, i + x)
                        to = (prev_find, prev_find + len(ex_a_buffer))
                        maps.append([ex_a_buffer, from_, to])
                        start = -1
                        ex_a_buffer = ""
            if ex_a_buffer:
                from_ = (start, end_a)
                to = (prev_find, prev_find + len(ex_a_buffer))
                maps.append([ex_a_buffer, from_, to])
            return maps

        def find_handler(y, z, end_a):
            maps = []
            next_index = -1
            start = y 
            x = 0
            indexes = []
            omitted = 1

            # Find conversion maps and return it
            for i in range(y, end_a):
                res = find(i, z, end_a)
                
                # Check if result is previous map shifted by one letter
                omit = False
                if maps:
                    # print("MA", maps)
                    map_req = []
                    # for map_ in maps[-1]:
                        # print("RES", res[0][0], maps[-1][i][0][i-1-start:], maps)
                        # map_ = maps[-1][i][0][i-1-start:]
                        # print("map==", map_ == res[0][0], next_index == i, next_index)
                    indexes = [(m[1][0] + omitted, m[1][1]) for m in maps[-1]]

                    for m in res:
                        # print("RES", m, next_index)
                        if m[1] in indexes:
                            next_index += 1
                            omit = True
                            omitted += 1
                            break
                if not omit:
                    maps.append(res)
                    # print("Not Omit")
                    next_index = i+1
                    # print("next_index", next_index, x)
            return maps

        return find_handler


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
    res = RegexGen('print("Hello", "World")', 'System.out.println("Hello World")', "python", "java")
    res = RegexGen('print("Another", "Example")', 'System.out.println("Another Example")', "python", "java")
    # res = RegexGen('print("Hello!")', 'System.out.println("Hello!")', "python", "java")
    # res = RegexGen('print("auto end return")', 'System.out.println("auto end return")', "python", "java")
    # res = RegexGen('print("rand")', 'System.out.println("rand")', "python", "java")
    # res = RegexGen("print('single quotes')", "System.out.println('single quotes')", "python", "java")
    # res = RegexGen('print("auto end return")', 'System.out.printf("auto end return\\n")', "python", "java")
    # res = RegexGen('print("Hello World 2")', 'System.out.println("Hello World 2")', "python", "java")
    # res = RegexGen('print("ABCD")', 'System.out.println("ABCD")', "python", "java")
    # res = RegexGen('print("Hello World Testing")', 'System.out.println("Hello World Testing")', "python", "java")
    # res = RegexGen('print(str(1) + str(2))', 'System.out.println(Integer.toString(1) + Integer.toString(2))', "python", "java")
    # res = RegexGen('math.sqrt(4)', 'Math.sqrt(4)', "python", "java")
    # res = RegexGen('print("Hello", end="\\n\\n")', 'System.out.println("Hello\\n\\n")', "python", "java")
    # res = RegexGen('print("HI", end="!\\n")', 'System.out.println("HI!")', "python", "java")
    # res = RegexGen('print("Good Bye", end=":(\\n")', 'System.out.println("Good Bye:(")', "python", "java")
    # res = RegexGen('print("3.14 ", end="This is the value of pi\\n")', 'System.out.println("3.14 This is the value of pi")', "python", "java")
    # res = RegexGen('print("Hours in day = ", end="24hrs - time wasted\\n")', 'System.out.println("Hours in day = 24hrs - time wasted")', "python", "java")
    

