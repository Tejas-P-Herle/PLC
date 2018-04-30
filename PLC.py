"""
Python Language Converter(PLC)
Converts Source Code from language A to B
"""
from language import Language
from error import Error
import logging
from file_path import FilePath
from language import Language

# Configure logging module
logging.basicConfig(filename="PLC_log.log", level=logging.DEBUG)

# Create variables for user input
user_input = {
    "file_path": None,
    "to_language": None,
    "output_file_name": None,
}


def PLC():
    """Main PLC application"""

    # Create user input string template
    input_msg = "{} or 'q' to abort: "

    # Create input messages
    input_file_path_msg = input_msg.format("Path to Program File")
    input_language_msg = input_msg.format("To Language")
    input_file_name_msg = input_msg.format("Output File Name")
    
    # Create variable to store function result
    from_language = None

    #
    # Get User Input
    # 

    validate_methods = [
        (FilePath.validate_file_path, "file_path", input_file_path_msg),
        (Language.validate, "to_language", input_language_msg),
        (FilePath.validate_file_name, "output_file_name", input_file_name_msg),
    ]

    # Validate user input
    for function, var_name, input_str in validate_methods:
        
        # Get input from user
        var, error = get_user_input(function, var_name, input_str)

        # If error encountered, print error and exit
        while error: 
            
            # Parse the error
            Error.parse(error, user_input=True)
            
            # Get input from user
            var, error = get_user_input(function, var_name, input_str)

        # Store latest value of var
        user_input[var_name] = var

        # If var_name is file_path recognize language of infile
        if var_name == "file_path":
            from_language = Language.recognize(var)

        # else if var_name is language,
        # store lower string(no capitals) of var_name
        elif var_name == "to_language":
            user_input[var_name] = var.lower()
    #
    # Start Conversion
    #

    # Make local variables for keys in user_input dict
    file_path = user_input['file_path']
    to_language = user_input['to_language']
    output_file_name = user_input['output_file_name']

    print(from_language, "->", to_language)
    return 0

def get_user_input(function, var_name, input_str):
    """Gets input from user and runs standard protocols"""

    # Get user input
    var = input(input_str)

    # Log debug message
    logging.debug("{} {}".format(var_name, var))

    # Check if user requests abort
    if var == "q":
        Error.parse("User Abort", user_input=True)
    
    # Define function parameters
    function_params = tuple([var])
    
    # Check for special cases
    if var_name == "output_file_name":     
        
        # Define function parameters
        function_params = (var, user_input['to_language'])
        
    # Run validation
    return var, function(*function_params)
    

def main():
    """Method run on file open(as main file)"""
    
    # Run PLC function
    PLC()


if __name__ == "__main__":
    main()
