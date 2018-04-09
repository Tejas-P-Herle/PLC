from converter.java_converter import JavaConverter
from converter.error import Error
from converter.mod_class import ModClass


default_options = {}


class Convert(ModClass):
    in_file = None
    out_file = None
    options = {}
    lang_class_dict = {'java': JavaConverter}

    def __init__(self, in_file, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Convert Class...')
        self.file = in_file
        self.print_v('in_file:', in_file)
        self.options = {}

        if type(options) != list or type(options[0]) != str:
            self.print_v('Options Parameter value:', options)
            func_name = 'Convert.__init__'
            param = 'options' if type(options) != list else 'options[0](Language)'
            val = 'options dict'
            Error(err_code_cls='02', err_code_sub_cls='01', err_code_desc='01',
                  raise_error=True, func_name=func_name, param=param, val=val)

        self.options['language'] = options[0].lower()
        self.print_v('To Convert Language:', self.options['language'])
        if self.options['language'] not in self.lang_class_dict.keys():
            lang = self.options['language']
            Error(err_code_cls='03', err_code_sub_cls='01', err_code_desc='01',
                  raise_error=True, lang=lang)

        self.out_file = self.convert()

    def convert(self):
        self.print_v('Convert Class: Method convert initiated')
        out_file = self.lang_class_dict[self.options['language']]()
        return out_file
