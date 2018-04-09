from converter.mod_class import ModClass
from converter.error import Error
from converter.status import Status


class Language(ModClass):
    lang_list = ['java', 'python', 'c', 'c++']
    lang_ext_list = ['.java', '.py', '.c', '.cpp']

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Language Class...')
        self.name = name
        self.ext = None

    @classmethod
    def get_lang(cls, file_name):
        cls.print_v('Language Class: Method get_lang initiated')
        ext = cls.get_ext(file_name)
        if ext not in cls.lang_ext_list:
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='03',
                  raise_error=True, ext=ext)
        return cls.lang_ext_list.index(ext)


    @classmethod
    def is_lang(cls, lang, raise_error=True):
        cls.print_v('Language Class: Method is_lang initiated')
        status = Status()
        if lang.lower() in cls.lang_list:
            status.condition = 'passed'
        else:
            status.condition = 'failed: Unknown Language'
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='01',
                  raise_error=raise_error, lang=lang)

    def file_lang_check(self, file_name, raise_error=True):
        self.print_v('Language Class: Method file_lang_check initiated')
        status = Status()
        try:
            self.ext = self.get_ext(file_name)
        except AttributeError:
            func_name = 'Language.file_lang_check'
            param = 'file_name'
            val = file_name
            Error(err_code_cls='02', err_code_sub_cls='01', err_code_desc='01',
                  raise_error=True, func_name=func_name, param=param, val=val)

        file_ext = self.get_ext(file_name)
        if self.ext != file_ext:
            status.condition = 'failed: Incorrect Extension'
            ext = file_ext
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='03',
                  raise_error=raise_error, ext=ext)
        else:
            status.condition = 'passed'

        return status

    @classmethod
    def get_ext(cls, file_name):
        cls.print_v('Language Class: Method get_ext initiated')
        return '.' + file_name.split('.')[-1]
