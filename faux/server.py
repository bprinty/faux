# -*- coding: utf-8 -*-
#
# Classes for setting up server mock.
#
# -----------------------------------


# imports
# -------
import os
import re
import six
import json
import time
import logging
import hashlib
from functools import wraps
from xml.etree import ElementTree
from threading import Thread


from .utils import format_data, request2path


# classes
# -------
class Server(object):
    """
    Object mimicking flask server to allow for spinning
    up server mock.
    """

    def __init__(self, *args, **kwargs):
        from flask import Flask

        self.cache = kwargs.pop('cache', None)
        self.flask = Flask(*args, **kwargs)
        # self.flask.logger.setLevel(logging.ERROR)
        if self.cache:
            self.init()
        return

    def init(self):
        """
        Method for decorating custom url handlers on server.
        """
        from flask import request, jsonify

        # general-purpose request handler
        @self.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def general(path):
            # format path
            path = request2path(path, args=request.args, payload=request.data)
            filename = os.path.join(self.cache, path)

            # if file doesn't exist, try to prepend the request method
            if not os.path.exists(filename):
                filename = os.path.join(self.cache, request.method.upper(), path)

            # if file exists, read and return
            if os.path.exists(filename) and not os.path.isdir(filename):
                with open(filename, 'r') as fi:
                    data = fi.read()
                return data

            return jsonify({'error': 'Could not find local resource!'}), 404


        # requests on root url
        @self.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def root():
            return general('.')


        # requests on root url with uuid
        @self.route('/<uuid:uuid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def ident(uuid):
            return general('_uuid')


        # requests on nested path with uuid
        @self.route('/<path:path>/<uuid:uuid>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def path_ident(path, uuid):
            return general(path + '/_uuid')


        # status url
        @self.route('/_/status', methods=['GET'])
        def status():
            return {"status": "ok"}

        return

    @property
    def logger(self):
        """
        Expose flask logger so user can change settings.

        TODO: update this class to use __getattr__ for defaulting
              to internal getattr(self.flask, item)
        """
        return self.flask.logger

    def route(self, *args, **kwargs):
        """
        Override flask route decorator to provide easier
        UX for return data. With these changes, users can
        simply return a dictionary or xml Element object instead
        of needing to craft a full response.
        """
        from flask import jsonify, Response

        # inner decorator to make return values easier
        def inner(method):
            @wraps(method)
            def _(*args, **kwargs):
                ret = method(*args, **kwargs)
                
                # json
                if isinstance(ret, dict):
                    ret = format_data(json.dumps(ret))
                    ret = json.loads(ret, strict=False)
                    return jsonify(ret), 200
                
                # xml
                elif isinstance(ret, ElementTree.Element):
                    ret = ElementTree.tostring(ret, encoding='utf8', method='xml')
                    ret = format_data(ret)
                    return Response(ret, mimetype='text/xml')
                
                # string
                elif isinstance(ret, six.string_types):
                    ret = format_data(ret)
                    return ret, 200

                # other data
                else:
                    return ret
            return _

        # proxy for using normal flask route decorator
        def decorator(func):
            return self.flask.route(*args, **kwargs)(inner(func))

        return decorator

    def run(self, **kwargs):
        # TODO: decorate all routes for reading from cached directory
        return Instance(self.flask, **kwargs)

    def __exit__(self, type, value, traceback):
        return


class Instance(object):
    """
    Contextmanager for running managing server mock.
    """

    def __init__(self, app, **kwargs):
        self.app = app
        kwargs['use_reloader'] = False
        self.thread = Thread(target=self.app.run, kwargs=kwargs)
        self.thread.daemon = True
        return

    def __enter__(self):
        self.thread.start()
        time.sleep(1)
        return self.thread

    def __exit__(self, type, value, traceback):
        return
