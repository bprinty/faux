# -*- coding: utf-8 -*-

__author__ = 'bprinty'
__email__ = 'bprinty@gmail.com'
__version__ = '0.0.2'


from .server import Server, request
from . import client as requests
from .client import get, post, put, delete, cache
