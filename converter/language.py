from mod_class import ModClass


class Language(ModClass):

    def __init__(self, name):
        self.name = name

    def check_file(self, file_name):
        
        try:
            self.ext
        except AttributeError:
            err_code_cls, err_code_sub_cls, err_desc = '04', '01', '01'
            err_code = err_code_cls + err_code_sub_cls + err_desc
            Error(err_code, raise_error=True)
        
        if self.ext != self.get_ext(file_name):
            return False

        #TODO

    def get_ext(file_name):
        return file_name.split('.')[-1]
