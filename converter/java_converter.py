from converter.file_class import File
from converter.language import Language


class Java(Language):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Java Class...')
        self.ext = '.java'
        self.file = File()
        # self.file.new_row()

    def convert_file(self, file):
        self.create_main_class()

    def create_main_class(self):
        pass
