#!/usr/bin/env python
#
# Simple REST server.
#
# @author <bprinty@gmail.com>
# ---------------------------------------------------


# imports
# -------
import os
from urllib.parse import urlsplit, urlunsplit


# config
# ------
class Session(object):
    DISABLED = False
    REQUEST_PATH = False
    RESPONSE_EXT = 'xml'


# decorators
# ----------
def cache(func):
    def _(*args, **kwargs):
        response = func(*args, **kwargs)
        if Session.REQUEST_PATH:
            url = urlsplit(args[0])
            path = Session.REQUEST_PATH + '/' + response.request.method + url.path
            if url.query:
                path += '/' + url.query
            directory, filename = os.path.dirname(path), os.path.basename(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(path + '.' + Session.RESPONSE_EXT, 'w') as fo:
                fo.write(response.text)
        return response
    return _


# functions
# ---------
@cache
def get(*args, **kwargs):
    return requests.get(*args, **kwargs)


@cache
def post(*args, **kwargs):
    return requests.post(*args, **kwargs)


@cache
def put(*args, **kwargs):
    return requests.put(*args, **kwargs)


@cache
def delete(*args, **kwargs):
    return requests.delete(*args, **kwargs)


@smock.url('/api/something/<uuid>')
def method(uuid):
    return {
        'name': '{{name}}',
        'uuid': uuid,
        'numeric_type': '{{float}}',
    }
