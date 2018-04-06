from file_class import File
from java_converter import JavaConverter, java_set_verbose
from options import Options
from error import Error


default_options = {}
verbose = None

def convert_set_verbose(val):
	global verbose
	verbose_val = (val == 'y')
	verbose = verbose_val
	java_set_verbose(verbose_val)

def print_v(*args, **kwargs):
	if verbose:
		print(*args, **kwargs)
	
class Convert:
	in_file = None
	out_file = None
	options = {}
	lang_class_dict = {'java': JavaConverter}
	
	def __init__(self, in_file, options):
		print_v('\nInitiating Convert Class...')
		self.file = in_file
		print_v('in_file:', in_file)
		self.options = Options()
		if type(options) != list or type(options[0]) != str:
			print_v('Options Parameter value:', options)
			err_code_cls, err_code_sub_cls, err_code_desc = '02', '01', '01'
			error_code = err_code_cls + err_code_sub_cls + err_code_desc
			function_name = 'Convert.__init__'
			parameter = 'options' if type(options) != list else 'options[0](Language)'
			Error(error_code, raise_error=True, function_name=function_name, parameter=parameter)
		self.options.language = options[0].lower()
		print_v('To Convert Language:', self.options.language)
		if self.options.language not in self.lang_class_dict.keys():
			print_v('Unknown Language:', self.options.language)
			err_code_cls, err_code_sub_cls, err_code_desc = '03', '01', '01'
			error_code = err_code_cls + err_code_sub_cls + err_code_desc
			language = self.options.language
			Error(error_code, raise_error=True, language=language)
		self.out_file = self.convert()
	
	def convert(self):
		out_file = self.lang_class_dict[self.options.language]()
		return out_file