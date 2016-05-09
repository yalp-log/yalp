# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
yalp.version
============

Get version of yalp
'''
from __future__ import print_function

from distutils.version import StrictVersion  # pylint: disable=E0611,F0401
__version__ = str(StrictVersion('1.10'))
del StrictVersion

if __name__ == '__main__':  # pragma: no cover
    print(__version__)
