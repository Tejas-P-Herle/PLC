"""Parse and Create custom Errors"""
import sys
from logger import Logger


plc_logger = Logger("error")


class Error:
    @staticmethod
    def parse(error_msg, user_input=False, quit_=False):
        """Parse errors(Handle Errors) and Quit(Optional)"""

        # Log error message
        plc_logger.log(error_msg, level="error")

        # Check if is user input
        if user_input:
            
            # If quit_ requested, print exit and quit_
            if error_msg == "Exitting":
                quit_ = True
            
            # Else respond to user with error message
            else:
                print(error_msg, end="\n\n")

        # If quit requested, quit with error_msg
        if quit_:
            if type(error_msg) == int:
                sys.exit(error_msg)
            else:
                sys.exit()

