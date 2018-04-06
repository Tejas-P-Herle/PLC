from status import Status

verbose = None

def input_set_verbose(val):
	global verbose
	verbose = (val == 'y')

def print_v(*args, **kwargs):
	if verbose:
		print(*args, **kwargs)
		

class Input:
	options = {}

	def __init__(self, options, *args, **kwargs):
		print_v('Input Class initiated')
		self.options = options
		self.status = Status()
		response = self.get_input(*args, **kwargs)
		self.response = response
		self.status.condition = 'passed'
		
	def get_input(self, *args, **kwargs):
		print_v('Input Class: Method get_input initiated')
		options = self.options
		text = options.text
		print_v('Input Text:', text)
		return input(text + ': ', *args, **kwargs)