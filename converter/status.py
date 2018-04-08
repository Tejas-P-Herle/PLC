from converter.mod_class import ModClass


class Status(ModClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Status Class...')
        self.condition = None
