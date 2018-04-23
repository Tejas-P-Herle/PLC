from converter.file_class import File
from converter.language import Language
from converter.bck import Bck


CURR_PATH = Language.curr_path


class Java(Language):
    lang = 'java'
    ext = '.java'
    cnv_dict_file = CURR_PATH + '\\java\\java_kw.txt'
    kw_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(super_init=True, *args, **kwargs)
        self.in_file = None
        self.file = File()
        self.main_cls = ''

    def convert(self, in_file, out_file_name):
        self.in_file = in_file
        self.read_cnv_dict()
        cmt_bck_list, code_bck_list = Bck.form_code_bck(self)
        cmt_bck_list = self.cvt_cmt_bck(cmt_bck_list)
        code_bck_list = self.del_main_call(code_bck_list)
        for i, bck in enumerate(code_bck_list):
            code_bck_list[i] = Bck.bck_ops(bck)
        self.file.file = self.make_java_code_str(cmt_bck_list, code_bck_list, out_file_name)
        return self.file

    @staticmethod
    def del_main_call(code_bck_list):
        for i, bck in enumerate(code_bck_list):
            if bck == [["if __name__ == '__main__':", '    main()']]:
                del code_bck_list[i]
        return code_bck_list

    @classmethod
    def make_java_code_str(cls, cmt_bck_list, code_bck_list, out_file_name):
        main_cls_bdy = ''
        for bck in code_bck_list:
            main_cls_bdy += bck
        main_cls = cls.create_main_cls(out_file_name)
        java_str = main_cls.format(main_cls_bdy=main_cls_bdy)
        return java_str

    @classmethod
    def cvt_cmt_bck(cls, bck):
        cmt_groups = cls.make_cmt_groups(bck)
        for group in cmt_groups:
            cls.cvt_cmt_group(group)
        return cmt_groups

    @staticmethod
    def make_cmt_groups(bck):
        cmt_groups = [[bck[0]]]
        j = 0
        for i in range(1, len(bck)):
            prev_cmt_loc = bck[i-1][0]
            cmt_loc = bck[i][0]
            if not ((prev_cmt_loc[2] == cmt_loc[2] is False) and (prev_cmt_loc[0] + 1 == cmt_loc[0])):
                j += 1
                cmt_groups.append([])
            cmt_groups[j].append(bck[i])

        return cmt_groups

    @staticmethod
    def cvt_cmt_group(cmt_group):
        if len(cmt_group) > 1 and not cmt_group[0][0][2]:
            cmt_group[0][1] = cmt_group[0][1].replace('#', '/*')
            for i in range(1, len(cmt_group)):
                cmt_group[i][1] = cmt_group[i][1].replace('#', ' *')
            last_cmt_ln = cmt_group[len(cmt_group) - 1][0][0]
            cmt_group.append([(last_cmt_ln + 1, cmt_group[0][0][1], False), ' */'])
        else:
            cmt_group[0][1] = cmt_group[0][1].replace('#', '//')

    @staticmethod
    def pop_all_cmt(file):
        cmt_list = []

        i = 0
        j = 0
        len_file = len(file)
        while j != len_file:
            file[i] = file[i].rstrip()
            ln = file[i]
            cmt_start = ln.find('#')
            is_in_ln = ln[:cmt_start].strip() != ''
            if cmt_start != -1:
                loc = (j, cmt_start, is_in_ln)
                cmt_list.append([loc, ln[cmt_start:]])
                file[i] = ln[:cmt_start]
            if file[i] == '':
                del file[i]
            elif file[i] == '\n':
                del file[i]
            else:
                i += 1
            j += 1

        return cmt_list, file

    @staticmethod
    def parse_code_bck(bck):
        bck = [bck] if isinstance(bck, str) else bck
        for i, ln in enumerate(bck):
            for kw in Java.kw_list:
                py_kw, java_kw = kw[0], kw[1]
                bck[i] = ln.replace(py_kw, java_kw) + ';'
        return bck

    @staticmethod
    def create_main_cls(out_file_name):
        main_cls_name = '.'.join(out_file_name.split('.')[0:-1])
        main_cls = ['public class {} {{{{\n'.format(main_cls_name),
                    '{main_cls_bdy}',
                    '}}']
        return ''.join(main_cls)
