import sys
import time
import os
from converter.mod_class import ModClass


CURR_PATH = os.path.dirname(os.path.realpath(__file__))


class Error(ModClass):
    err_cls_dict = {}
    err_sub_cls_dict = {}
    err_desc_dict = {}
    err_dict = {0: err_cls_dict, 1: err_sub_cls_dict, 2: err_desc_dict}

    def __init__(self, err_code_cls, err_code_sub_cls, err_code_desc, raise_error=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.print_v('\nInitiating Error Class...')

        self.print_v('Reading Error DB...')
        self.read_err_db()

        self.print_v('Sorting Error code')
        err_sec = []
        err_code_sub_cls = err_code_cls + err_code_sub_cls
        err_code_desc = err_code_sub_cls + err_code_desc
        i = 0
        for err_sec_cont, err_sec_code in {'err_cls': err_code_cls,
                                           'err_sub_cls': err_code_sub_cls,
                                           'err_desc': err_code_desc}.items():
            self.print_v('Getting {}...'.format(err_sec_cont))
            err_sec.append(self.get_err_code_sec(err_sec_code, i, err_sec_cont))
            i += 1

        self.err_cls = err_cls = err_sec[0]
        self.err_sub_cls = err_sub_cls = err_sec[1]
        self.err_desc = err_desc = err_sec[2]

        self.print_v('Replacing Key Words...')
        if kwargs:
            for key, value in kwargs.items():
                err_desc = self.replace(err_desc, key, value)
            self.err_desc = err_desc

        self.print_v('Forming Print Message...')
        err_msg = '{}[{}]: {}'.format(err_cls, err_sub_cls, err_desc)

        self.print_v('Logging Error...')
        log_file_path = CURR_PATH.replace('converter', 'err.log')
        sys.stderr = open(log_file_path, 'a+')
        log_text = '[{}] {}\n'.format(time.asctime(time.localtime(time.time())).replace('  ', ' '), err_msg)
        sys.stderr.write(log_text)

        if raise_error:
            self.print_v('Raising Error...\n')
            print(err_msg)

            sys.exit(1)

    @classmethod
    def replace(cls, err_msg, key, val):
        cls.print_v('Error Class: Method replace initiated')

        cls.print_v('Replacing key words')
        key = '{' + key + '}'
        return err_msg.replace(key, val)

    @classmethod
    def read_err_db(cls):
        cls.print_v('Error Class: Method read_err_db initiated')

        cls.print_v('Reading File...')
        err_db_path = CURR_PATH + '\\err_db.txt'
        with open(err_db_path, 'r') as file:
            err_db = list(map(lambda x: x.replace('\n', '').replace(',', ''), file.readlines()))

            cls.print_v('Splitting Sections...')
            err_db_sec = cls.split_sec(err_db)

            cls.print_v('Storing Error Sections...')
            for i in range(len(err_db_sec)):
                cls.store_err(i, err_db_sec[i])

    @classmethod
    def split_sec(cls, err_db):
        cls.print_v('Error Class: Method split_sec initiated')
        err_db_sec = [[], [], []]

        cls.print_v('Splitting sections...')
        sec_no = 0
        for line in err_db:
            if not line == '#':
                err_db_sec[sec_no].append(line)
            else:
                sec_no += 1

        return err_db_sec

    @classmethod
    def store_err(cls, sec_no, sec):
        cls.print_v('Error Class: Method store_err initiated')
        sec_dict = cls.err_dict[sec_no]

        cls.print_v('Storing error section...')
        for line in sec:
            line_split = line.split(': ', 1)
            sec_dict[line_split[0]] = line_split[1]

    def get_err_code_sec(self, err_sec_code, err_sec_num, err_cont):
        self.print_v('Error Class: Method get_err_code initiated')
        self.print_v('{}_code: {}'.format(err_cont, err_sec_code))

        self.print_v('Getting Section')
        if err_sec_code in self.err_dict[err_sec_num].keys():
            err_sec = self.err_dict[err_sec_num][err_sec_code]
        else:
            err_sec = 'Unknown Error'

        self.print_v('{}: {}'.format(err_cont, err_sec))
        return err_sec
