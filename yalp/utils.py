# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.utils
==========
'''
EMPTY = object()


def new_method_proxy(func):
    ''' Proxy function call to lazy get attrs '''
    def inner(self, *args):                # pylint: disable=C0111
        if self._wrapped is EMPTY:         # pylint: disable=W0212
            self._setup()                  # pylint: disable=W0212
        return func(self._wrapped, *args)  # pylint: disable=W0212
    return inner


class LazyObject(object):
    '''
    Wrapper for another class to delay instantiation.
    '''
    def __init__(self):
        self._wrapped = EMPTY

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is EMPTY:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise TypeError('can\'t delete _wrapped.')
        if self._wrapped is EMPTY:
            self._setup()
        delattr(self._wrapped, name)

    def _setup(self):
        '''
        Must be implemented by subclasses to initialize wrapped object.
        '''
        raise NotImplementedError

    __members__ = property(lambda self: self.__dir__())
    __dir__ = new_method_proxy(dir)
