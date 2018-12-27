# -*- coding: utf-8 -*-
#
# Session management.
#
# ------------------------------------------------


# imports
# -------
import os
import logging
from gems import cached
import json
from functools import wraps
import requests
from requests.packages import urllib3
try:
    import cookielib as cookiejar
except ImportError:
    import http.cookiejar as cookiejar

import six.moves.urllib as urllib

from requests import ConnectionError

from .utils import debugtime


# config
# ------
SESSION = dict()



# methods
# -------
def options(**kwargs):
    """
    Set global options for session management. You can also configure the system
    to use a default options file located in ``~/.lab7/client.yml``. Here's an example
    options file:

    .. code-block:: console

        $ cat ~/.lab7/client.yml

        email: me@localhost
        password: password
        cache: false


    Args:
        host (str): Host with database to connect to.
        port (int): Port to connect to database with.
        email (str): Username to access application with.
        password (str): Password to be used with username.
        cookies (str): Optional path to cookies file to store session data.
        cache (bool): Whether or not to cache objects for faster querying.


    Examples:
        >>> # set default options for connections
        >>> import esp
        >>> esp.options(
        >>>     email='user@localhost', password='pass'
        >>>     cookies='/path/to/cookies-file.txt'
        >>> )
        >>>
        >>> # interact with esp client normally
        >>> from esp.models import Protocol
        >>> obj = Protocol('My Protocol')
    """
    import os
    from gems import composite
    global SESSION, CONFIG

    # load defaults
    CONFIG = composite(dict(
        host='127.0.0.1',
        port=8002,
        email='admin@localhost',
        password='password',
        cookies=None,
        cache=True,
        ssl=False,

    ))

    # load user config
    USER = os.path.join(os.getenv('HOME', os.path.expanduser('~')), '.lab7', 'client.yml')
    if os.path.exists(USER):
        CONFIG += composite.from_yaml(open(USER))

    # load specified config
    if 'config' in kwargs and os.path.exists(kwargs['config']):
        CONFIG += composite.from_yaml(open(kwargs['config']))
        del kwargs['config']

    # overwrite with any additional options
    CONFIG += composite({k: v for k, v in kwargs.items()})

    # configure url (if specified)
    if 'url' in kwargs:
        parsed = urllib.parse.urlparse(kwargs['url'])
        netloc = parsed.netloc.split(':')
        CONFIG.ssl = parsed.scheme == 'https'
        CONFIG.host = netloc[0]
        CONFIG.port = None if len(netloc) == 1 else int(netloc[1])

    # establish session
    SESSION = Session(
        host=CONFIG.host,
        port=CONFIG.port,
        cookies=CONFIG.cookies,
        email=CONFIG.email,
        password=CONFIG.password,
        ssl=CONFIG.ssl,
        cache=CONFIG.cache
    )
    return CONFIG


options()
