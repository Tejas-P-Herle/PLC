"""Gets output of print statement(stdout) and stderr"""
import sys
from io import StringIO


class GetIO:
    def __init__(self):
        """Initiate GetIO class"""

        # Store default stderr and stdout values
        self.default_stderr = sys.stderr
        self.default_stdout = sys.stdout
        
        # Save if stdout is default
        self.reset = True

        # Declare variables for storing line count
        self.stdout_line_count = 0
        self.stderr_line_count = 0

        # Stubs stdout
        self.stub_output()

    def stub_output(self):
        """Replaces stdout and stderr with StringIO"""
        
        # Replace system stderr and stdout to StringIO
        sys.stderr = StringIO()
        sys.stdout = StringIO()

        # Store change
        self.reset = False

    def reset_output(self):
        """Resets stdout and stderr to default"""
        
        # Reset stdout to default value
        sys.stderr = self.default_stderr
        sys.stdout = self.default_stdout

        # Stores reset
        self.reset = True

    def read_stdout(self, return_line_count=False):
        """Reads stdout and returns value"""
        
        # If stdout is not set to default read stdout
        if not self.reset:
            value = sys.stdout.getvalue()
            self.truncate_stdout()
            self.stdout_line_count += 1
            if return_line_count:
                return value, self.stdout_line_count
            return value

    def read_stderr(self):
        """Reads stderr and returns value"""
        
        # If stderr is not set to default read stderr
        if not self.reset:
            value = sys.stderr.getvalue()
            self.truncate_stderr()
            return value

    def read_output(self):
        """Reads both stdout and stderr and returns value"""

        # Read both stdout and stderr
        return self.read_stdout(), self.read_stderr()

    def print(self, *args, **kwargs):
        """Print to console"""

        # Temporarily set stdout to default and print string
        sys.stdout = self.default_stdout
        print(*args, **kwargs)
        sys.stdout = StringIO()

    @staticmethod
    def truncate_stdout():
        """Truncate StringIO object buffer for stdout"""

        # Truncate stdout
        sys.stdout.truncate(0)
        sys.stdout.seek(0)

    @staticmethod
    def truncate_stderr():
        """Truncate StringIO object buffer for stderr"""

        # Truncate and set cursor to 0
        sys.stderr.truncate(0)
        sys.stderr.seek(0)

    def truncate(self):
        """Truncate both stdout and stderr"""
        
        # Truncate stdout
        self.truncate_stdout()

        # Truncate stderr
        self.truncate_stderr()
    
    def reset_stdout_line_count(self):
        self.stdout_line_count = 0

