import sys
from file_class import File, file_set_verbose
from convert import Convert, convert_set_verbose
from options import Options, options_set_verbose


verbose_options = {'ask': False, 'verbose_value': 'y'}


def main():
	print("Main function of program 'python_to_java.py' has been initiate")
	if verbose_options['ask']:
		verbose = input('Verbose<Y/N>: ').lower()
		while verbose not in ['y', 'n']:
			verbose = input("Please input only 'Y' or 'N': ").lower()
		print('Setting verbose to', verbose == 'y')
		set_verbose(verbose)
	else:
		set_verbose(verbose_options['verbose_value'])
	print('Requesting in_file paramaters')
	in_file = File().get_file()
	# 'python_file.py'
	print('\nin_file:', in_file.name)
	print('\nGetting options for convertion...')
	options = Options.get('default conversion')
	print('\nInitiating convertions of in_file')
	out_file = Convert(in_file, options)
	print('\nGetting options for out_file...')
	options = Options.get('default out_file')
	print('\nInitiating file write...')
	File.write_file(out_file, options)
	print('\nProgram Execution Successful. Press any key to continue...')
	return 0
	
def set_verbose(verbose):
	file_set_verbose(verbose)
	convert_set_verbose(verbose)
	options_set_verbose(verbose)
	
if __name__ == '__main__':
	main()
	input()