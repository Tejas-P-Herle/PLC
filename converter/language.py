from converter.error import Error
from converter.status import Status


class Language:
    lang_list = ['java', 'python', 'c', 'c++']
    lang_ext_list = ['.java', '.py', '.c', '.cpp']
    ext = None
    lang = None

    def __init__(self, *args, **kwargs):
        try:
            if kwargs['super_init']:
                return
        except KeyError:
            pass

        lang = kwargs['lang']

        self.lang_cls = []
        sub_cls = Language.__subclasses__()
        for cls in sub_cls:
            if cls.lang == lang:
                lang_cls = cls
                self.lang_inst = lang_cls()
                return

    @classmethod
    def get_lang(cls, file_name):
        ext = cls.get_ext(file_name, check=False)
        if ext not in cls.lang_ext_list:
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='03',
                  raise_error=True, ext=ext)
        return cls.lang_ext_list.index(ext)

    @classmethod
    def is_lang(cls, lang, raise_error=True):
        status = Status()
        if lang.lower() in cls.lang_list:
            status.condition = 'passed'
        else:
            status.condition = 'failed: Unknown Language'
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='01',
                  raise_error=raise_error, lang=lang)

        return status

    def file_lang_check(self, file_name, raise_error=True):

        try:
            self.ext = self.get_ext(file_name)
        except AttributeError:
            func_name = 'Language.file_lang_check'
            param = 'file_name'
            val = file_name
            Error(err_code_cls='02', err_code_sub_cls='01', err_code_desc='01',
                  raise_error=True, func_name=func_name, param=param, val=val)

        ext, valid = self.get_ext(file_name, raise_error=raise_error, check=True)

        status = Status()
        if valid:
            status.condition = 'failed: Incorrect Extension'
        else:
            status.condition = 'passed'

        return status

    @classmethod
    def get_ext(cls, file_name, check=True, raise_error=True):
        ext = '.' + file_name.split('.')[-1]

        if check:
            status = cls.check_ext(ext, raise_error=raise_error)
            valid = True
            if status.condition != 'passed':
                valid = False
            return ext, valid
        return ext

    @classmethod
    def check_ext(cls, ext, raise_error=True):
        status = Status()
        if ext not in cls.lang_ext_list:
            status.condition = 'failed: Incorrect extension'
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='03',
                  raise_error=raise_error, ext=ext)
        else:
            status.condition = 'passed'
        return status

    def is_lang_file(self, file_name, raise_error=True):

        ext = self.get_ext(file_name, raise_error=False, check=False)

        status = Status()
        if self.lang_inst.ext != ext:
            status.condition = 'failed: Incorrect extension'
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='03',
                  raise_error=raise_error, ext=ext)
        else:
            status.condition = 'passed'
        return status

    def convert(self, in_file, out_file_name):
        return self.lang_inst.convert(in_file, out_file_name)
