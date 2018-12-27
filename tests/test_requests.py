# -*- coding: utf-8 -*-
#
# Testing for server caching.
# 
# ------------------------------------------------


# imports
# -------
import unittest
import pytest


# fixtures
# --------
@pytest.fixture(scope='session')
def external():
    """
    Set up mock server for testing request caching.
    """

    # imports
    import os
    import logging
    from multiprocessing import Process
    from flask import Flask, jsonify, request, make_response
    

    # setup
    app = Flask(__name__)
    app.logger.setLevel(logging.ERROR)


    # define routes for testing
    @app.route('/simple')
    def simple():
        """
        Simple endpint with get/post
        """
        ret = {'status': 'ok'}
        ret.update(request.args)
        return jsonify(ret), 200

    @app.route('/nested/<param>')
    def nested(param):
        """
        Manage server state.
        """
        ret = {'param': param, 'status': 'ok'}
        ret.update(request.args)
        return jsonify(ret), 200


    # set up class for managing spawned processes
    class Janitor(object):
        def __enter__(self):
            os.setpgrp()
        def __exit__(self, type, value, traceback):
            import signal
            try:
                os.killpg(0, signal.SIGKILL)
            except KeyboardInterrupt:
              pass


    # run the server and wait 
    with Janitor():
        Process(target=app.run, kwargs=dict(
            host='0.0.0.0',
            debug=True,
            port=1927,
        )).start()

        yield
    return


# @pytest.fixture(scope='session')
# def mock():
#     from . import SANDBOX
#     with smock.run(port=1928, cache=SANDBOX):
#         yield
#     return



# tests
# -----
@pytest.mark.usefixtures("external")
class TestDataPull(unittest.TestCase):

    def test__status(self):
        import requests
        res = requests.get('http://localhost:1927/simple')
        self.assertEqual(res.json()['status'], 'ok')
        return

    # # GET
    # def test_get_simple(self):
    #     requests.get()
    #     get('http://localhost/')
    #     return

    # def test_get_simple_args(self):
    #     return

    # def test_get_nested(self):
    #     return

    # def test_get_nested_param(self):
    #     return

    # def test_get_nested_param_args(self):
    #     return

    # # POST
    # def test_post_simple(self):
    #     return

    # def test_post_simple_args(self):
    #     return

    # def test_post_nested(self):
    #     return

    # def test_post_nested_param(self):
    #     return

    # def test_post_nested_param_args(self):
    #     return

    # # PUT
    # def test_put_simple(self):
    #     return

    # def test_put_simple_args(self):
    #     return

    # def test_put_nested(self):
    #     return

    # def test_put_nested_param(self):
    #     return

    # def test_put_nested_param_args(self):
    #     return

