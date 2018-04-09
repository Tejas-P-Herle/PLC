from converter.status import Status
from converter.mod_class import ModClass
from converter.error import Error


class Input(ModClass):
    options = {}

    def __init__(self, text, check_func=None, raise_error=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Input Class...')
        self.status = Status()
        response = self.get_input(text)
        self.response = response
        if check_func:
            self.status.condition = check_func(response, raise_error=raise_error).condition
        else:
            self.status.condition = 'passed'
        self.check_input(raise_error=raise_error, query=text)

    def get_input(self, text):
        self.print_v('Input Class: Method get_input initiated')
        self.print_v('Input Text:', text)
        return input(text + ': ')

    def check_input(self, raise_error, query):
        self.print_v('Input Class: Method check_input initiated')
        if self.status.condition != 'passed':
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='02',
                  raise_error=raise_error, query=query)
