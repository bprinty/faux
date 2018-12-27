# -*- coding: utf-8 -*-

__author__ = 'bprinty'
__email__ = 'bprinty@gmail.com'
__version__ = '0.0.1'




# imports
# -------
import os
import logging
from multiprocessing import Process
from flask import Flask, jsonify, request, make_response



# config
# ------
app = Flask(__name__)
app.logger.setLevel(logging.ERROR)


# classes
# -------
class Janitor(object):

    def __enter__(self):
        os.setpgrp()

    def __exit__(self, type, value, traceback):
        import signal
        try:
            os.killpg(0, signal.SIGKILL)
        except KeyboardInterrupt:
          pass


class Server(object):

    def __enter__(self):
        # self() in background?
        return

    def __call__(self, *args, **kwargs):
        # serve in foreground?
        return

    def run(self, host='0.0.0.0', port=8100, debug=True, cache='/tmp'):
        self.cache = cache
        app = Flask()
        with Janitor():
            Process(target=app.run, kwargs=dict(
                port=port,
                debug=debug,
                host=host,
            )).start()
        return

    def __exit__(self, type, value, traceback):
        return


def route(*args, **kwargs):
    return app.route
