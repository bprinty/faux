#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# package setup
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# config
# ------
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import smock


# files
# -----
with open('requirements.txt') as fi:
    requirements = fi.readlines()

with open('tests/requirements.txt') as fi:
    test_requirements = fi.readlines()

with open('README.rst') as readme_file:
    readme = readme_file.read()


# exec
# ----
setup(
    name='smock',
    version=smock.__version__,
    description="Quick and easy server mocking.",
    long_description=readme,
    author="bprinty",
    author_email='bprinty@gmail.com',
    url='https://github.com/bprinty/smock',
    packages=[
        'smock',
    ],
    package_dir={'smock':
                 'smock'},
    include_package_data=True,
    install_requires=requirements,
    keywords='smock',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nosetests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'smock = smock.__main__:main'
        ],
    }
)
