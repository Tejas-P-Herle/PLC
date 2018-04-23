from converter.bck import Bck


class For:
    @classmethod
    def cvt_for(cls, for_bck):
        for_head = cls.get_for_head(for_bck)
        for_bdy = cls.get_for_bdy(for_bck)
        return for_head.format(for_bdy=for_bdy)

    @classmethod
    def get_for_bdy(cls, for_bck):
        for_bdy = for_bck[1:]
        for_bdy_str = ''
        for i, bck in enumerate(for_bdy):
            bck_func = Bck.identify_bck(bck)
            for_bdy[i] = bck_func(bck)
            for ln in for_bdy[i]:
                for_bdy_str += ln
        return for_bdy_str

    @classmethod
    def get_for_head(cls, for_bck):
        fst_ln = Bck.get_fst_ln(for_bck)
        var, iterable = fst_ln.split(' in ')
        var = var.strip('for ')
        if iterable.find('range') != -1:
            range_param = iterable[iterable.find('(') + 1: iterable.find(')')].split(', ')

            start = 0
            step = 1

            if len(range_param) == 2:
                start, end = range_param
            elif len(range_param) == 3:
                start, end, step = range_param
            else:
                end = range_param[0]
            for_loop_str = 'for (int {var}={start}; {var} < {end}; {var} += {step})'
            return for_loop_str.format(var=var, start=start, end=end, step=step) + '{{\n{for_bdy}\n}}'
