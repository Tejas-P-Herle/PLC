import re
from converter.bck import Bck


class Func:
    @classmethod
    def cvt_func(cls, func_bck):
        java_func_str = '{func_head} {{{func_bdy}}}'
        fst_ln = Bck.get_fst_ln(func_bck)
        main_func = fst_ln.find('def main') != -1
        if main_func:
            func_head = 'public static void main(String[] args) {{\n{main_func_bdy}\n' + ' ' * 4 + '}}\n'
        else:
            func_head = cls.get_func_head(func_bck)
        func_bdy = cls.get_func_bdy(func_bck)
        java_func_str = java_func_str.format(func_head=func_head, func_bdy=func_bdy)
        return java_func_str

    @classmethod
    def get_func_bdy(cls, bck):
        del bck[0][0]
        func_bdy = bck
        func_bdy_str = ''
        for bck in func_bdy:
            bck_func = Bck.identify_bck(bck)
            bck = bck_func(bck)
            for ln in bck:
                func_bdy_str += ln
        return func_bdy_str

    @classmethod
    def get_func_head(cls, bck):
        func_args = cls.get_func_args(bck)
        bck = bck.strip('def ')
        index = bck.find('(')
        modifier = 'public static'
        return_type = cls.get_return_type(bck)
        func_dcl = '{} {} {}'.format(modifier, return_type, bck[:index + 1] + func_args + ') {{{func_bdy}}}')
        return func_dcl

    @classmethod
    def get_return_type(cls, bck):
        return_type = bck.split(' -> ')[-1][:-1]
        for python_arg, java_arg in {'str': 'String', 'None': 'void'}.items():
            return_type = return_type.replace(python_arg, java_arg)
        return return_type

    @classmethod
    def get_func_args(cls, func_bck):
        start_index = func_bck.find('(') + 1
        end_index = func_bck.find(')')
        arg_str = func_bck[start_index:end_index]
        args_list = arg_str.split(', ')
        args_python = cls.get_args_list(args_list)
        args = cls.cvt_java_args_str(args_python)
        return args

    @staticmethod
    def get_args_list(args_list):
        args = {}
        for arg in args_list:
            arg_name, arg_type = arg.split(': ')
            args[arg_name] = arg_type
        return args

    @staticmethod
    def cvt_java_args_str(args_python):
        args_java = {}
        for arg, arg_type in args_python.items():
            for python_dt, java_dt in {'str': 'String', ' list': '[]'}.items():
                arg_type = re.sub('[\'"]', '', arg_type.replace(python_dt, java_dt))
            args_java[arg] = arg_type
        args_java_str = ''
        for arg_name, arg_type in args_java.items():
            args_java_str += '{} {}, '.format(arg_type, arg_name)
        return args_java_str[:-2]