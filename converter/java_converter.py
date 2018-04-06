from file_class import File
from mod_class import ModClass

	
class JavaConverter(ModClass):
	file = []
	
	def __init__(self):
		self.print_v('\nInitiating JavaConverter Class...')
		#self.file.new_row()
		
	def convert_file(self, file):
		self.create_main_class()
		
	def create_main_class(self):
		pass
