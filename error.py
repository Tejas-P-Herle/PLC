"""Parse and Create custom Errors"""
import sys
import logging

logging.basicConfig(filename="PLC_log.log", level=logging.DEBUG)


class Error:
    @staticmethod
    def parse(error_msg, user_input=False, quit_=False):
        """Parse errors(Handle Errors) and Quit(Optional)"""
        # Log error message
        logging.error(error_msg)

        # Check if is user input
        if user_input:
            
            # If quit_ requested, print abort and quit_
            if error_msg == "User Abort":
                quit_ = True
            
            # Else respond to user with error message
            else:
                print(error_msg, end="\n\n")

        # If quit requested, quit with error_msg
        if quit_:
            sys.exit(error_msg)

