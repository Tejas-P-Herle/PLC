from converter.status import Status
from converter.error import Error


class Input:
    options = {}

    def __init__(self, text, check_func=None, raise_error=True, *args, **kwargs):
        self.status = Status()
        resp = self.get_input(text)
        self.resp = resp
        if check_func:
            self.status.condition = check_func(resp, raise_error=raise_error).condition
        else:
            self.status.condition = 'passed'
        self.check_input(raise_error=raise_error, query=text)

    @staticmethod
    def get_input(text):
        return input(text + ': ')

    def check_input(self, raise_error, query):
        if self.status.condition != 'passed':
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='02',
                  raise_error=raise_error, query=query)
