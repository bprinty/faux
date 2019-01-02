#!/usr/bin/env python
#
# Simple REST server.
#
# @author <bprinty@gmail.com>
# ---------------------------------------------------


# imports
# -------
import os
import requests
from functools import wraps
try:
    from urllib.parse import urlsplit, urlunsplit, parse_qsl
except ImportError:
    from urlparse import urlsplit, urlunsplit, parse_qsl

from .utils import request2path


# config
# ------
CACHE = None


def cache(path):
    """
    Method for setting options during request session.

    Example:
        >>> from faux import requests
        >>> requests.cache('/path/to/local/cache')
        >>> requests.get('http://localhost')
    """
    global CACHE
    if not path:
        raise AssertionError('Invalid path specified for cache directory ("{}")!'.format(path))
    CACHE = path
    return


# decorators
# ----------
def cache_response(func):
    """
    Decorator for caching requests submitted with this module
    into a file structure that can be served by a mock server.
    """
    @wraps(getattr(requests, func.__name__))
    def _(*args, **kwargs):
        global CACHE
        response = func(*args, **kwargs)
        if CACHE:

            # generate local url
            url = urlsplit(args[0])
            rpath = request2path(
                url=url.path,
                args=dict(parse_qsl(url.query)),
                payload=response.request.body
            )
            # for some reason, os.path.join(cache, method, rpath) doesn't work?
            path = os.path.join(CACHE, response.request.method.upper()) + '/' + rpath
            
            # make location if it doesn't exist
            directory, filename = os.path.dirname(path), os.path.basename(path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # write the data
            with open(path, 'w') as fo:
                fo.write(response.text)

        return response
    return _


# functions
# ---------
@cache_response
def get(*args, **kwargs):
    return requests.get(*args, **kwargs)


@cache_response
def post(*args, **kwargs):
    return requests.post(*args, **kwargs)


@cache_response
def put(*args, **kwargs):
    return requests.put(*args, **kwargs)


@cache_response
def delete(*args, **kwargs):
    return requests.delete(*args, **kwargs)

