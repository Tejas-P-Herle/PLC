from converter.error import Error
from converter.status import Status
from os import path


CURR_PATH = path.dirname(path.realpath(__file__))


class Language:
    lang_list = ['java', 'python', 'c', 'c++']
    lang_ext_list = ['.java', '.py', '.c', '.cpp']
    ext = None
    lang = None
    cnv_dict_file = None
    curr_path = CURR_PATH
    kw_list = []

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

    @staticmethod
    def split_secs(bck):
        sec_index = [1]
        j = 0
        ln_lvl = [int((len(ln) - len(ln.lstrip(' '))) / 4) for ln in bck]
        min_lvl = min(ln_lvl)
        base_lvl = min_lvl if ln_lvl.count(min_lvl) != 1 else min_lvl + 1
        last_lvl = False
        len_ln = len(ln_lvl)

        for i in range(1, len_ln):
            lvl_down = ln_lvl[i] == base_lvl == ln_lvl[i - 1] - 1
            if i != len_ln - 1:
                lvl_up = ln_lvl[i] == base_lvl == ln_lvl[i + 1] - 1
                lvl_change = lvl_up or lvl_down
            else:
                lvl_change = lvl_down
            if lvl_change:
                sec_index.append(i)
                j += 1
            sec_index[j] += 1
        sec_index[-1] += 1
        sec_bck_list = [bck[i:j] for i, j in zip([0] + sec_index, sec_index)]

        if sec_bck_list[0] == bck:
            sec_bck_list = sec_bck_list[0]
            last_lvl = True

        return sec_bck_list, last_lvl

    @staticmethod
    def rm_void_ln(bck):
        i = 0
        while i < len(bck):
            if bck[i].strip() == '':
                del bck[i]
            else:
                i += 1

        return bck

    def read_cnv_dict(self):
        with open(self.cnv_dict_file, 'r') as file:
            lns = [(ln.replace('\n', '').split(' => ')) for ln in file.readlines()]
            for from_kw, to_kw in lns:
                self.kw_list.append((from_kw, to_kw))

    def rec_split_bck(self, bck_in, fst_lvl):
        bck_list = []
        if fst_lvl:
            for i in bck_in:
                bck_list.append([])
        for i, bck in enumerate(bck_in):
            bck, last_lvl = self.split_secs(bck)
            if not last_lvl:
                bck_list_lcl = self.rec_split_bck(bck, False)
            else:
                bck_list_lcl = [bck]
            if fst_lvl:
                bck_list[i] += bck_list_lcl
            else:
                bck_list += bck_list_lcl
        return bck_list

    def convert(self, in_file, out_file_name):
        return self.lang_inst.convert(in_file, out_file_name)
