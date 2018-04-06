from file_class import File


verbose = None

def java_set_verbose(val):
	global verbose
	verbose = (val == 'y')

def print_v(*args, **kwargs):
	if verbose:
		print(*args, **kwargs)
	
class JavaConverter:
	file = []
	
	def __init__(self):
		print_v('\nInitiating JavaConverter Class...')
		#self.file.new_row()
		
	def convert_file(self, file):
		self.create_main_class()
		
	def create_main_class(self):
		pass