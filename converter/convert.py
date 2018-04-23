from converter.language import Language
from converter.error import Error


default_options = {}


class Convert:
    in_file = None
    out_file = None
    options = {}

    def __init__(self, in_file, options_cnv, options_out_file, *args, **kwargs):
        self.options = dict()

        lang = options_cnv['lang'].resp.lower()
        options = options_cnv['lang'].options

        out_file_name = options_out_file['out_file_name'].resp

        if type(options) != dict:
            func_name = 'Convert.__init__'
            param = 'options'
            val = 'options dict'
            Error(err_code_cls='02', err_code_sub_cls='01', err_code_desc='01',
                  raise_error=True, func_name=func_name, param=param, val=val)

        lang = Language(lang=lang)

        self.file = lang.convert(in_file, out_file_name)
