import os
from input_cls import Input
from status import Status
from error import Error
from options import Options
from mod_class import ModClass


print_option = 'f'


class File(ModClass):
    file = []
    
    def __init__(self):
        self.print_v('\n')
        
    @classmethod
    def get_file(cls):
        cls.print_v("File Class: Method get_file initiated")
        file_path = cls.get_file_path()
        cls.print_v('file_path:', file_path)
        file = File()
        file.open(file_path)
        return file
        
    @classmethod
    def get_file_path(cls):
        cls.print_v("File Class: Method get_file_path initiated")
        cls.print_v('Requesting file path')
        text = 'Source File Path'
        options = Options()
        options.text = text
        user_input = Input(options)
        cls.print_v('Checking input status')
        if user_input.status.condition != 'passed':
            raise RuntimeError('Input Error')
        # TODO Make own error
        cls.print_v('Retrieving file path')
        response = user_input.response
        cls.print_v('Checking file_path validity')
        status = cls.check_file_path(response)
        if status.condition != 'passed':
            self.print_v('Incorrect file_path')
            raise ValueError('Incorrect file path value')
        file_path = response
        cls.print_v('file_path:', file_path)
        return file_path
    
    @classmethod
    def get_file_name(cls, file_path):
        cls.print_v('File Class: Method get_file_name initiated')
        cls.print_v('In file_path:', file_path)
        file_name = file_path.split('\\')[-1]
        cls.print_v('File Name:', file_name)
        return file_name
    
    @classmethod
    def check_file_path(cls, file_path, raise_error=True):
        cls.print_v('File Class: Method check_file_path initiated')
        status = Status()
        cls.print_v('Calling class method isfile...')
        file_exists = cls.isfile(file_path)
        if not file_exists:
            cls.print_v("File doesn't exist")
            cls.print_v('Raising error File opetaion error...')
            status.condition = 'failed'
            err_code_cls, err_code_sub_cls, err_code_desc = '01', '01', '01'
            error_code = err_code_cls + err_code_sub_cls + err_code_desc
            status.error = Error(error_code, raise_error, file_path=file_path)
        # TODO Perform file_path validation
        else:
            cls.print_v('File exists')
            status.condition = 'passed'
        return status
    
    @classmethod    
    def isfile(cls, file_path):
        cls.print_v('File Class: Method is_file initiated')
        try:
            cls.print_v('Checking if file exits...')
            file_exists = os.path.isfile(file_path)
        except Exception as e:
            cls.print_v('os.path.isfile check exception')
            raise e
        return file_exists
    
    @classmethod
    def write_file(self, file, options):
        pass
        
    def open(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_lines = file.readlines()
                self.file = file_lines
                self.name = self.get_file_name(file_path)
                self.print_v('File name:', self.name)
                self.length = len(file_lines)
                self.print_v('File Length: {} lines'.format(self.length))
                if print_option == 'o':
                    options = Options()
                    options.detail = 'overview'
                    options.overview = Options()
                    options.overview.lines = 2
                else:
                    options = Options()
                    options.detail = 'full'
                self.print_file(options)
        except Exception as e:
            raise e
            
    def print_file(self, options):
        if options.detail == 'full':
            self.print_v('File Lines(All):\n' + ''.join(self.file) + '\n---EOF---')
        elif options.detail == 'overview':
            no_of_lines = options.overview.lines
            self.print_v('no_of_lines:', no_of_lines)
            if no_of_lines >= self.length - 2 and no_of_lines <= self.length:
                self.print_v('File Lines(All):\n' + ''.join(self.file) + '\n---EOF---')
            elif no_of_lines > self.length - 2:
                err_code_cls, err_code_sub_cls, err_code_desc = '01', '02', '01'
                error_code = err_code_cls + err_code_sub_cls + err_code_desc
                Error(error_code, raise_error=True, file_name=self.name)
            else:
                self.print_v('File Lines(Overview):\n' + ''.join(self.file[0:no_of_lines]), end='')
                self.print_v('....')
                self.print_v(''.join(self.file[-2:]) + '\n---EOF---')
        
    def write_line(self, line):
        pass
        
    def new_row(self):
        pass