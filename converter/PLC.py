from converter.file_class import File
from converter.convert import Convert
from converter.input_cls import Input
from converter.language import Language


def main():
    in_file = File().get_file()
    print('\nin_file:', in_file.name)

    options_cnv = dict()
    cnv_queries = {'lang': ['Language(To Convert)', Language.is_lang]}
    for var_name, query in cnv_queries.items():
        options_cnv[var_name] = Input(query[0], check_func=query[1], raise_error=True)
    lang = options_cnv['lang'].resp

    options_out_file = dict()
    out_file_queries = {'out_file_name': ['Output File Name', Language(lang=lang).is_lang_file]}
    for var_name, query in out_file_queries.items():
        options_out_file[var_name] = Input(query[0], check_func=query[1], raise_error=True)
    
    print('\nInitiating conversions of in_file...')
    conversion = Convert(in_file, options_cnv, options_out_file)
    print('File successfully converted')
    
    print('\nInitiating file write...')
    conversion.file.write_file(options_out_file, mode='w')
    print('File Write Successful')
    
    print('\nProgram Execution Successful. Press any key to continue...')
    return 0


if __name__ == '__main__':
    main()
    input()
