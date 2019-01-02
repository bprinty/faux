# -*- coding: utf-8 -*-

import os


TESTS = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.realpath(os.path.join(TESTS, '..'))
RESOURCES = os.path.join(TESTS, 'resources')
SANDBOX = os.path.join(TESTS, 'sandbox')

class config:
    URL = None
    PORT = None

