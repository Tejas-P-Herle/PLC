verbose = None

def status_set_verbose(val):
	global verbose
	verbose = (val == 'y')

def print_v(*args, **kwargs):
	if verbose:
		print(*args, **kwargs)


class Status:
	def __init__(self):
		self.condition = None