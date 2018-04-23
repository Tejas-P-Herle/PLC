class Bck:
    @staticmethod
    def get_fst_ln(in_bck):
        bck = in_bck[0]
        while type(bck) == list:
            bck = bck[0]
        return bck

    @classmethod
    def identify_bck(cls, bck):
        from converter.java.func_cls import Func
        from converter.java.for_cls import For
        from converter.java.java import Java

        fst_ln = cls.get_fst_ln(bck).strip()
        for kw, func in {'def': Func.cvt_func, 'for': For.cvt_for}.items():
            if fst_ln.find(kw) != -1:
                return func
        else:
            return Java.parse_code_bck

    @classmethod
    def bck_ops(cls, bck):
        bck_func = cls.identify_bck(bck)
        bck = bck_func(bck)
        return bck

    @classmethod
    def form_code_bck(cls, lang_cls):
        in_file_ln = lang_cls.in_file.file

        cmt_list, in_file_ln = lang_cls.pop_all_cmt(in_file_ln)
        in_file_ln = lang_cls.rm_void_ln(in_file_ln)
        main_bck, last_lev = lang_cls.split_secs(in_file_ln)
        if not last_lev:
            code_bck = lang_cls.rec_split_bck(main_bck, True)
        else:
            code_bck = main_bck
        return cmt_list, code_bck
