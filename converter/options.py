from input_cls import Input
from object import Object, object_set_verbose
from error import Error

verbose = None
default_file_options = Object()
default_file_options.request_options = ['Output File Name']
										
default_convert_options = Object()
default_convert_options.request_options = ['To Conversion Language']

def options_set_verbose(val):
	global verbose
	object_set_verbose(val)
	verbose = (val == 'y')

def print_v(*args, **kwargs):
	if verbose:
		print(*args, **kwargs)


class Options:
	def __init__(self):
		print_v('\n')
	
	@classmethod
	def get(cls, options):
		print_v('Options Class: Method get initiated')
		if type(options) == str:
			if options == 'default conversion':
				options = default_convert_options
			elif options == 'default out_file':
				options = default_file_options
			else:
				print_v('Unknown default key code')
				err_code_cls, err_code_sub_cls, err_code_desc = '02', '01', '01'
				error_code = err_code_cls + err_code_sub_cls + err_code_desc
				function_name = 'Options.get'
				parameter = 'options'
				Error(error_code, raise_error=True, function_name=function_name, parameter=parameter)
		response_list = []
		for option in options.request_options:
			options_obj = Options()
			options_obj.text = option
			print_v('Requesting input:', options_obj.text)
			user_input = cls.get_input(options_obj)
			print_v('Checking input status')
			if user_input.status.condition != 'passed':
				raise RuntimeError('Input Error')
			#TODO
			print_v('Check passed')
			response_list.append(user_input.response)
		print_v('response_list:', response_list)
		return response_list
		
	@classmethod
	def get_input(cls, options):
		print_v('Options Class: Method get_input initiated')
		print_v('options:', options.text)
		response = Input(options)
		print_v('Checking response validity')
		print_v('TODO')
		#TODO
		return response
		
		