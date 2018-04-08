from converter.file_class import File
from converter.mod_class import ModClass


class JavaConverter(ModClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating JavaConverter Class...')
        self.file = File()
        # self.file.new_row()

    def convert_file(self, file):
        self.create_main_class()

    def create_main_class(self):
        pass
