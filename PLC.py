"""
Python Language Converter(PLC)
Converts Source Code from language A to B
"""
from language import Language
from error import Error
import logging

logging.basicConfig(filename='PLC_log.log', level=logging.DEBUG)


def main():

    # Get Input Program File Path
    file_path = input('Path to Program File: ')
    
    # Get To Conversion Language
    to_language = input('To Language: ')
    
    # Get Output file name
    output_file_name = input('Output File Name: ')

    logging.debug('file_path', file_path)
    logging.debug('to_language', to_language)
    logging.debug('output_file_name', output_file_name)

    #
    # Validate Inputs
    #

    # Validate File Path
    error = FilePath.validate_file_path(file_path)
    
    # If error encountered, print error and exit
    if error: Error.parse_error()

    # Validate to conversion language
    error = Language.validate(language)

    # If error encountered, print error and exit
    if error: Error.parse_error()

    # Validate output file name
    FilePath.validate_file_name(output_file_name)
    
    # If error encountered, print error and exit
    if error: Error.parse_error()

    #
    # Start Conversion
    #

    # Recognize Language
    from_language = Language.recognize(file_path)
    print(from_language, '->', to_language)
    return 0


if __name__ == '__main__':
    main()
