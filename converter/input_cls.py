from status import Status
from mod_class import ModClass


class Input(ModClass):
	options = {}

	def __init__(self, options, *args, **kwargs):
		self.print_v('Input Class initiated')
		self.options = options
		self.status = Status()
		response = self.get_input(*args, **kwargs)
		self.response = response
		self.status.condition = 'passed'
		
	def get_input(self, *args, **kwargs):
		self.print_v('Input Class: Method get_input initiated')
		options = self.options
		text = options.text
		self.print_v('Input Text:', text)
		return input(text + ': ', *args, **kwargs)
