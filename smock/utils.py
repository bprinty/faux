# -*- coding: utf-8 -*-
#
# Utility methods for module.
#
# ----------------------------------


# imports
# -------
import re
import hashlib
from faker import Faker


# config
# ------
factory = Faker()
factory.uuid = factory.uuid4


# functions
# ---------
def format_data(string):
    for outer, inner in re.findall(r'({{.*?(\w+).*?}})', string):
        if hasattr(factory, inner):
            inner = getattr(factory, inner)()
            string = string.replace(outer, inner)
    return string


def free_port():
    import socket
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1]


def request2path(url, args=None, payload=None):
    """
    Encode request into filepath recognizable by
    framework when serving requests.
    """
    path = url + '/'

    # convert args into queryable filename
    if args:
        for key in sorted(args.keys()):
            path += key + '=' + args[key] + '&'
        path = path[:-1]

    # convert payload into queryable hash postfix
    if payload:
        res = re.sub(r"\s+", "", ''.join(sorted(str(payload))))
        hc = hashlib.md5(res.encode('ascii')).hexdigest()
        hc = hc[:7]
        path += hc
    
    # final formatting
    if path[-1] == '/':
        path = path[:-1]
    return path