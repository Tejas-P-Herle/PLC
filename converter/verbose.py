class Verbose:
    verbose = False

    def __init__(self):
        self.print_v('Initiating Verbose Class...')

    @classmethod
    def print_v(cls, *args, **kwargs):
        if cls.verbose:
            print(*args, **kwargs)
