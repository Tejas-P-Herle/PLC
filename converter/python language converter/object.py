verbose = None

def object_set_verbose(val):
	global verbose
	verbose = (val == 'y')

def print_v(*args, **kwargs):
	if verbose:
		print(*args, **kwargs)

		
class Object():
	def __init__(self):
		pass