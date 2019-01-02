# -*- coding: utf-8 -*-
#
# pytest plugins
#
# ------------------------------------------------


# imports
# -------
import pytest
from . import config


# config
# ------
def pytest_addoption(parser):
    return


def pytest_configure(config):
    return


# fixtures
# --------
@pytest.fixture(autouse=True, scope='session')
def bootstrap():
    """
    Global test setup/teardown fixture.
    """
    from faux.utils import free_port
    config.PORT = free_port()
    config.URL = 'http://localhost:{}'.format(config.PORT)

    yield

    import os
    import shutil
    from . import SANDBOX
    if os.path.exists(SANDBOX):
        shutil.rmtree(SANDBOX)
    return


@pytest.fixture(scope='session')
def server():
    """
    Set up mock server for testing request caching.
    """

    # imports
    import logging
    from faux import Server, request
    from . import config, RESOURCES
    
    # set up app
    app = Server(__name__, cache=RESOURCES)
    app.logger.setLevel(logging.INFO)


    # define routes for testing
    @app.route('/simple', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def simple():
        """
        Simple endpint with get/post
        """
        ret = {
            'status': 'ok',
            'uuid': '{{uuid}}',
        }
        if request.args:
            ret.update(request.args)
        if request.json:
            ret.update(request.json)
        return ret

    @app.route('/nested/<param>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def nested(param):
        """
        Manage server state.
        """
        ret = {
            'status': 'ok',
            'param': param,
            'uuid': '{{uuid}}'
        }
        if request.args:
            ret.update(request.args)
        if request.json:
            ret.update(request.json)
        return ret


    # run server in the background for testing
    with app.run(port=config.PORT, debug=True):
        yield
    return
