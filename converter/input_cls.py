from converter.status import Status
from converter.mod_class import ModClass


class Input(ModClass):
    options = {}

    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Input Class...')
        self.options = options
        self.status = Status()
        response = self.get_input()
        self.response = response
        self.status.condition = 'passed'

    def get_input(self):
        self.print_v('Input Class: Method get_input initiated')
        options = self.options
        text = options.text
        self.print_v('Input Text:', text)
        return input(text + ': ')
