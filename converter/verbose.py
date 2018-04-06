class Verbose:
    verbose = False

    def __init__(self, verbose):
        self.verbose = verbose

    @classmethod
    def print_v(cls, *args, **kwargs):
        if cls.verbose:
            print(*args, **kwargs)
