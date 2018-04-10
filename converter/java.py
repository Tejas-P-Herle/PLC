from converter.file_class import File
from converter.language import Language


class Java(Language):
    lang = 'java'
    ext = '.java'

    def __init__(self, *args, **kwargs):
        super().__init__(super_init=True, *args, **kwargs)
        self.file = File()

    def convert(self, file, out_file_name):
        self.create_main_cls(file, out_file_name)
        return self.file

    def create_main_cls(self, file, out_file_name):
        main_cls_name = '.'.join(out_file_name.split('.')[0:-1]).upper()
        main_cls = ['public class {} {{\n'.format(main_cls_name),
                    'public static void main(String[] args) {\n',
                    '}\n',
                    '}']
        for line in main_cls:
            self.file.write_line(line)
