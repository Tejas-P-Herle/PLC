import sys
import time
import os


CURR_PATH = os.path.dirname(os.path.realpath(__file__))


class Error:
    err_cls_dict = {}
    err_sub_cls_dict = {}
    err_desc_dict = {}
    err_dict = {0: err_cls_dict, 1: err_sub_cls_dict, 2: err_desc_dict}

    def __init__(self, err_code_cls, err_code_sub_cls, err_code_desc, raise_error=True, *args, **kwargs):

        self.read_err_db()

        err_sec = []
        err_code_sub_cls = err_code_cls + err_code_sub_cls
        err_code_desc = err_code_sub_cls + err_code_desc
        i = 0
        for err_sec_cont, err_sec_code in {'err_cls': err_code_cls,
                                           'err_sub_cls': err_code_sub_cls,
                                           'err_desc': err_code_desc}.items():
            err_sec.append(self.get_err_code_sec(err_sec_code, i, err_sec_cont))
            i += 1

        self.err_cls = err_cls = err_sec[0]
        self.err_sub_cls = err_sub_cls = err_sec[1]
        self.err_desc = err_desc = err_sec[2]

        if kwargs:
            for key, value in kwargs.items():
                err_desc = self.replace(err_desc, key, value)
            self.err_desc = err_desc

        err_msg = '{}[{}]: {}'.format(err_cls, err_sub_cls, err_desc)

        log_file_path = CURR_PATH.replace('converter', 'err.log')
        sys.stderr = open(log_file_path, 'a+')
        log_text = '[{}] {}\n'.format(time.asctime(time.localtime(time.time())).replace('  ', ' '), err_msg)
        sys.stderr.write(log_text)

        if raise_error:
            print(err_msg)

            sys.exit(1)

    @classmethod
    def replace(cls, err_msg, key, val):

        key = '{' + key + '}'
        return err_msg.replace(key, val)

    @classmethod
    def read_err_db(cls):

        err_db_path = CURR_PATH + '\\err_db.txt'
        with open(err_db_path, 'r') as file:
            err_db = list(map(lambda x: x.replace('\n', '').replace(',', ''), file.readlines()))

            err_db_sec = cls.split_sec(err_db)

            for i in range(len(err_db_sec)):
                cls.store_err(i, err_db_sec[i])

    @classmethod
    def split_sec(cls, err_db):
        err_db_sec = [[], [], []]

        sec_no = 0
        for line in err_db:
            if not line == '#':
                err_db_sec[sec_no].append(line)
            else:
                sec_no += 1

        return err_db_sec

    @classmethod
    def store_err(cls, sec_no, sec):
        sec_dict = cls.err_dict[sec_no]

        for line in sec:
            line_split = line.split(': ', 1)
            sec_dict[line_split[0]] = line_split[1]

    def get_err_code_sec(self, err_sec_code, err_sec_num, err_cont):

        if err_sec_code in self.err_dict[err_sec_num].keys():
            err_sec = self.err_dict[err_sec_num][err_sec_code]
        else:
            err_sec = 'Unknown Error'

        return err_sec
