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

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

import smock


# files
# -----
with open('README.md') as readme_file:
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
            'smock = smock.server:run'
        ],
    }
)
