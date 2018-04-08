from converter.input_cls import Input
from converter.object import Object
from converter.error import Error
from converter.mod_class import ModClass


verbose = None
default_file_options = Object()
default_file_options.request_options = ['Output File Name']

default_convert_options = Object()
default_convert_options.request_options = ['To Conversion Language']


class Options(ModClass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Options Class...')
        self.detail = None
        self.text = None
        self.print_v('\n')

    @classmethod
    def get(cls, options):
        cls.print_v('Options Class: Method get initiated')
        if type(options) == str:
            if options == 'default conversion':
                options = default_convert_options
            elif options == 'default out_file':
                options = default_file_options
            else:
                cls.print_v('Unknown default key code')
                err_code_cls, err_code_sub_cls, err_code_desc = '02', '01', '01'
                error_code = err_code_cls + err_code_sub_cls + err_code_desc
                function_name = 'Options.get'
                parameter = 'options'
                Error(error_code, raise_error=True, function_name=function_name, parameter=parameter)
        response_list = []
        for option in options.request_options:
            options_obj = Options()
            options_obj.text = option
            cls.print_v('Requesting input:', options_obj.text)
            user_input = cls.get_input(options_obj)
            cls.print_v('Checking input status')
            if user_input.status.condition != 'passed':
                raise RuntimeError('Input Error')
            # TODO
            cls.print_v('Check passed')
            response_list.append(user_input.response)
        cls.print_v('response_list:', response_list)
        return response_list

    @classmethod
    def get_input(cls, options):
        cls.print_v('Options Class: Method get_input initiated')
        cls.print_v('options:', options.text)
        response = Input(options)
        cls.print_v('Checking response validity')
        cls.print_v('TODO')
        # TODO
        return response
