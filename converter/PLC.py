from converter.file_class import File
from converter.convert import Convert
from converter.mod_class import ModClass
from converter.input_cls import Input
from converter.language import Language


verbose_options = {'ask': False, 'verbose_value': 'y'}


def main():
    print("Main function of program 'python_to_java.py' has been initiate")
    if verbose_options['ask']:
        verbose = input('Verbose<Y/N>: ').lower()
        
        while verbose not in ['y', 'n']:
            verbose = input("Please input only 'Y' or 'N': ").lower()

        verbose = verbose == 'y'
    else:
        verbose = verbose_options['verbose_value']
    
    print('Setting verbose to', verbose)
    set_verbose(verbose)
    
    print('Requesting in_file parameters')
    in_file = File().get_file()
    print('\nin_file:', in_file.name)
    
    print('\nGetting options for conversion...')
    options = dict()
    cnv_queries = {'lang': ['Language(To Convert)', Language.is_lang]}
    for var_name, query in cnv_queries.items():
        options[var_name] = Input(query[0], check_func=query[1], raise_error=True)
    
    print('\nInitiating conversions of in_file')
    out_file = Convert(in_file, options)
    
    print('\nGetting options for out_file...')
    options = dict()
    out_file_queries = {'out_file_name': ['Output File Name', File.check_file_path]}
    for var_name, query in out_file_queries.items():
        options[var_name] = Input(query[0], check_func=query[1], raise_error=True)
    
    print('\nInitiating file write...')
    File.write_file(out_file, options)
    
    print('\nProgram Execution Successful. Press any key to continue...')
    return 0


def set_verbose(verbose):
    ModClass.verbose = verbose


if __name__ == '__main__':
    main()
    input()
