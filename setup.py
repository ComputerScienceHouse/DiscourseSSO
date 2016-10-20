#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='DiscourseOIDC',
    version='0.1.0',
    license='Apache2.0',
    description='SSO Discourse Application to allow SAML authentication',
    long_description='%s' % read('README.md'),
    author='Steven Mirabito & Marco Fargetta',
    author_email='smirabito@csh.rit.edu',
    url='https://github.com/ComputerScienceHouse/DiscourseOIDC',
#    packages=find_packages(exclude=['tests*']),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        'OpenID Connect', 'oidc', 'discourse'
    ],
    install_requires=[
        'Flask>=0.10.1',
        'Flask-pyoidc>=1.0.0',
        'gunicorn'
    ],
    extras_require={
        # eg: 'rst': ['docutils>=0.11'],
    },
    entry_points={
        'console_scripts': [
            'discroursesso = sso.__main__:main'
        ]
    },
)
