from converter.mod_class import ModClass


class ABC(ModClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating ABC Class...')
