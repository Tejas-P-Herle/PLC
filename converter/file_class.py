import os
from converter.input_cls import Input
from converter.status import Status
from converter.error import Error


class File:
    file = []
    
    def __init__(self, *args, **kwargs):
        self.file = self.create_file()
        self.length = None
        self.name = None
        
    @classmethod
    def get_file(cls):
        file_path = cls.get_file_path()
        file = File()
        file.open(file_path)
        return file
        
    @classmethod
    def get_file_path(cls):
        text = 'Source File Path'
        usr_input = Input(text, cls.check_file_path, raise_error=True)
        file_path = usr_input.resp
        return file_path
    
    @classmethod
    def get_file_name(cls, file_path):
        file_name = file_path.split('\\')[-1]
        return file_name
    
    @classmethod
    def check_file_path(cls, file_path, raise_error=True):
        status = Status()
        file_exists = cls.isfile(file_path)
        if not file_exists:
            status.condition = 'failed'
            status.error = Error(err_code_cls='01', err_code_sub_cls='01', err_code_desc='01',
                                 raise_error=raise_error, file_path=file_path)
        else:
            status.condition = 'passed'
        return status
    
    @classmethod    
    def isfile(cls, file_path):
        try:
            file_exists = os.path.isfile(file_path)
        except Exception as e:
            raise e
        return file_exists

    def write_file(self, options, mode='w'):
        out_file_name = options['out_file_name'].resp
        with open(out_file_name, mode) as file:
            file_str = ''.join(self.file)
            file.write(file_str)
        
    def open(self, file_path):

        with open(file_path, 'r') as file:
            self.file = file.readlines()
            self.name = self.get_file_name(file_path)
            self.length = len(self.file)

    @staticmethod
    def create_file():
        file = []
        return file
        
    def write_line(self, line):
        self.file.append(line)
