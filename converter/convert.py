from file_class import File
from java_converter import JavaConverter
from options import Options
from error import Error
from mod_class import ModClass


default_options = {}

	
class Convert(ModClass):
	in_file = None
	out_file = None
	options = {}
	lang_class_dict = {'java': JavaConverter}
	
	def __init__(self, in_file, options):
		self.print_v('\nInitiating Convert Class...')
		self.file = in_file
		self.print_v('in_file:', in_file)
		self.options = Options()
		if type(options) != list or type(options[0]) != str:
			self.print_v('Options Parameter value:', options)
			err_code_cls, err_code_sub_cls, err_code_desc = '02', '01', '01'
			error_code = err_code_cls + err_code_sub_cls + err_code_desc
			function_name = 'Convert.__init__'
			parameter = 'options' if type(options) != list else 'options[0](Language)'
			Error(error_code, raise_error=True, function_name=function_name, parameter=parameter)
		self.options.language = options[0].lower()
		self.print_v('To Convert Language:', self.options.language)
		if self.options.language not in self.lang_class_dict.keys():
			self.print_v('Unknown Language:', self.options.language)
			err_code_cls, err_code_sub_cls, err_code_desc = '03', '01', '01'
			error_code = err_code_cls + err_code_sub_cls + err_code_desc
			language = self.options.language
			Error(error_code, raise_error=True, language=language)
		self.out_file = self.convert()
	
	def convert(self):
		out_file = self.lang_class_dict[self.options.language]()
		return out_file
