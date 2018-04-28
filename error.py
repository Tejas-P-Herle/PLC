"""Parse and Create custom Errors"""
import sys
import logging

logging.basicConfig(filename='PLC_log.log', level=logging.DEBUG)


class Error:
    @staticmethod
    def parse(error_msg, quit=False):
        """Parse errors(Handle Errors) and Quit(Optional)"""
        # Log error message
        logging.error(error_msg)
        if quit:
            sys.exit(error_msg)

