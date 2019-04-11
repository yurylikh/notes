import abc
import re


def indented(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        return re.sub(r'(^|\n)(?=.)', Substitute(), res) if '\n' in res else res
    return wrapper


class Substitute(object):
    def __init__(self):
        self.ind_width = 4
        self.shift = ' ' * self.ind_width

    def __call__(self, match_obj):
        return '\n' + self.shift


class Wrapper:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, obj):
        self.obj = obj
        self.open = self.close = ''

    def __str__(self):
        return self.open + self.split(self.obj) + self.close

    def split(self, obj):
        if isinstance(obj, (list, tuple)):
            return ',\n'.join(obj) + '\n'
        if isinstance(obj, (str, unicode)):
            return obj


class QuotesWrapper(Wrapper):
    def __init__(self, obj):
        super(QuotesWrapper, self).__init__(obj)
        self.open = self.close = '"'


class CurlyBracesWrapper(Wrapper):
    def __init__(self, obj):
        super(CurlyBracesWrapper, self).__init__(obj)
        self.open, self.close = '{', '}'

@indented
def f(s):
    return 'SYNTAX ' + str(s)



if __name__ == '__main__':

    s = 'Hello, Yury'
    print QuotesWrapper(s)
    
    l = ('a', 'b', 'c')
    print f(CurlyBracesWrapper(l))
