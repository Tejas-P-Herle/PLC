#!/usr/bin/env python3

"""
Python Language Converter(PLC)
Converts Source Code from language A to B
"""
from error import Error
from logger import Logger
from file_path import FilePath
from language import Language
from code_processor import CodeProcessor
from get_corrections import GetCorrections

# Initialize plc_logger
plc_logger = Logger("PLC")

# Create variables for user input
user_input = {
    "file_path": None,
    "lang_from": None,
    "lang_to": None,
    "output_file_name": None,
}

# Create variable to store corrections
corrections = GetCorrections()
code_processer = None


def PLC():
    """Main PLC application"""

    global code_processor

    # Create user input string template
    input_msg = "{} or 'q' to abort: "

    # Create input messages
    input_file_path_msg = input_msg.format("Path to Program File")
    input_language_msg = input_msg.format("To Language")
    input_file_name_msg = input_msg.format("Output File Path")
    
    # Create variable to store function result
    lang_from = None

    #
    # Get User Input
    #

    validate_methods = [
        (FilePath.validate_file_path, "file_path", input_file_path_msg),
        (Language.validate, "lang_to", input_language_msg),
        (FilePath.validate_file_name, "outfile_path", input_file_name_msg),
    ]

    # Validate user input
    for func, var_name, input_str in validate_methods:

        # Get input from user
        user_input_val, error = get_user_input(func, var_name, input_str)

        user_input_val = str(user_input_val)

        # Check if input is currently at to language 
        # and input language is same as output language
        if var_name == "lang_to" and user_input_val.lower() == lang_from:
            error = "Language of file is same as to conversion language"

        # If error encountered, print error and exit
        while error:

            # Parse the error
            Error.parse(error, user_input=True)

            # Get input from user
            user_input_val, error = get_user_input(func, var_name, input_str)

            # Check if input is currently at to language 
            # and input language is same as output language
            if var_name == "lang_to" and user_input_val.lower() == lang_from:
                error = "Language of file is same as to conversion language"

        # Store latest value of var
        user_input[var_name] = user_input_val

        # If var_name is file_path recognize language of infile
        if var_name == "file_path":
            lang_from = Language.recognize(user_input_val)

        # else if var_name is language,
        # store lowercase string of var_name
        elif var_name == "lang_to":
            user_input[var_name] = user_input_val.lower()
    #
    # Start Conversion
    #

    # Make local variables for keys in user_input dict
    file_path = user_input['file_path']
    lang_to = user_input['lang_to']
    outfile_path = user_input['outfile_path']
    user_input['lang_from'] = lang_from

    print(lang_from, "->", lang_to)

    # Create code processor instance
    code_processor = CodeProcessor(file_path, lang_from, lang_to,
                                   outfile_path, corrections)

    # Run convert method of code processor
    code_processor.convert()

    # Write converted file to disk
    error = code_processor.write_file_to_disk()

    # Check if error occurred
    if error:
        if error == 5:
            Error.parse(5, quit_ = True)
        Error.parse(error, user_input=False)

    return 0


def get_user_input(func, var_name, input_str):
    """Gets input from user and runs standard protocols"""

    # Get user input
    var = str(input(input_str))

    # Log debug message
    plc_logger.log("VAR[NAME]", var_name, var)

    # Check if user requests abort
    if var == "q":
        Error.parse("User Abort", user_input=True)

    # Define function parameters
    function_params = tuple([var])

    # Check for special cases
    if var_name == "outfile_path":

        # Define function parameters
        function_params = (var, user_input['lang_to'])

    # Run validation
    return var, func(*function_params)

def implement_corrections():
    """Implement the corrections learnt from the user"""

    global code_processor

    # Read new conversions from data base
    code_processor.read_conv_db()

    # Run the new conversions
    code_processor.run_regex_conversion()

    # Write the outputfile to disk
    code_processor.write_file_to_disk(ask_overwrite=1)


def main():
    """Function run on file open"""

    # Run PLC function
    PLC()

    # Request corrections for unknown conversion
    corrections.get()

    # Learn corrections
    corrections.digest(user_input["lang_from"], user_input["lang_to"])

    # Implement corrections
    implement_corrections()



if __name__ == "__main__":
    main()
