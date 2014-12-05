# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp
====
'''


class BaseYalp(object):
    '''
    Base yalp class.
    '''
    def __init__(self, type_=None, **kwargs):  # pylint: disable=W0613
        super(BaseYalp, self).__init__()
        self.type_ = type_
