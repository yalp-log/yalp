#!/usr/bin/env python
# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
Setup script for yalp
'''

import os
from setuptools import setup, find_packages

# Ensure we are in yalp source dir
SETUP_DIRNAME = os.path.dirname(__file__)
if SETUP_DIRNAME != '':
    os.chdir(SETUP_DIRNAME)

YALP_VERSION = os.path.join(os.path.abspath(SETUP_DIRNAME),
                            'yalp',
                            'version.py')
YALP_REQS = os.path.join(os.path.abspath(SETUP_DIRNAME),
                         'requirements.txt')

# pylint: disable=W0122
exec(compile(open(YALP_VERSION).read(), YALP_VERSION, 'exec'))
# pylint: enable=W0122

VER = __version__  # pylint: disable=E0602

REQUIREMENTS = []
with open(YALP_REQS) as rfh:
    for line in rfh.readlines():
        if not line or line.startswith('#'):
            continue
        REQUIREMENTS.append(line.strip())


SETUP_KWARGS = {
    'name': 'yalp',
    'version': VER,
    'url': 'https://github.com/yalp-log/yalp',
    'license': 'Apache-2',
    'description': 'Distributed log parsing and collection.',
    'author': 'Timothy Messier',
    'author_email': 'tim.messier@gmail.com',
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
    ],
    'packages': find_packages(exclude=[
        '*.tests*', '*.tests.*', 'tests.*', 'tests',
    ]),
    'package_data': {},
    'data_files': [],
    'scripts': [
        'scripts/yalp',
        'scripts/yalp-inputs',
        'scripts/yalp-parsers',
        'scripts/yalp-outputers',
    ],
    'install_requires': REQUIREMENTS,
    'zip_safe': False,
}

if __name__ == '__main__':
    setup(**SETUP_KWARGS)
