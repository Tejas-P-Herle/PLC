import sys
from converter.mod_class import ModClass


class Error(ModClass):
    error_class_dict = {'01': 'File Operation Error',
                        '02': 'Input Parameter Error',
                        '03': 'User Input Error'}
    error_sub_class_dict = {'0101': 'File Not Found', '0102': 'File Read Error', '0201': 'Parameter Value Error',
                            '0301': 'Input Value Error'}
    error_description_dict = {'010101': 'Target File {file_path} was not found',
                              '010201': 'Failed to read target file {file_name}',
                              '020101': "Invalid value for '{function_name}' function, input parameter '{parameter}'",
                              '030101': "Unknown Language: '{language}'"}
    error_dict = {0: error_class_dict, 1: error_sub_class_dict, 2: error_description_dict}

    def __init__(self, error_code, raise_error=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Error Class...')
        self.print_v('Getting error_class...')
        error_class = self.get_error_class(error_code)
        self.error_class = error_class
        self.print_v('Getting error_sub_class...')
        error_sub_class = self.get_error_sub_class(error_code)
        self.error_sub_class = error_sub_class
        self.print_v('Getting error_description...')
        error_description = self.get_error_description(error_code)
        if kwargs:
            for key, value in kwargs.items():
                key = '{' + key + '}'
                error_description = error_description.replace(key, value)
        self.error_description = error_description

        if raise_error:
            self.print_v('Raising Error...')
            print('\n{}[{}]: {}\n'.format(error_class, error_sub_class, error_description))

            sys.exit('error_code: {}'.format(error_code))

    def get_error_class(self, error_code):
        error_class_section_start = 0
        return self.get_error_code_section(error_code, error_class_section_start)

    def get_error_sub_class(self, error_code):
        error_sub_class_section_start = 2
        return self.get_error_code_section(error_code, error_sub_class_section_start)

    def get_error_description(self, error_code):
        error_description_section_start = 4
        return self.get_error_code_section(error_code, error_description_section_start)

    def get_error_code_section(self, error_code, section_start):
        error_section_code = error_code[0: section_start + 2]
        if section_start == 0:
            error_section_content = 'error_class'
        elif section_start == 2:
            error_section_content = 'error_sub_class'
        elif section_start == 4:
            error_section_content = 'error_description'
        else:
            raise ValueError('Invalid error section_start value')
        self.print_v('{}_code: {}'.format(error_section_content, error_section_code))
        error_section_number = section_start / 2
        if error_section_code in self.error_dict[error_section_number].keys():
            error_section = self.error_dict[error_section_number][error_section_code]
        else:
            error_section = 'Unknown Error'
        self.print_v('{}: {}'.format(error_section_content, error_section))
        return error_section
