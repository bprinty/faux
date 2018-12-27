#!/usr/bin/env python
#
# Simple REST server.
#
# @author <bprinty@gmail.com>
# ---------------------------------------------------


# imports
# -------
import os
from flask import Flask, jsonify, request, make_response
from flask.ext.httpauth import HTTPBasicAuth


# init
# ----
config = {
    'auth': False,
    'debug': True,
    'port': 9999,
    'users': {
        'user': 'pass'
    }
}
app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

# disable authentication (if specified)
if not config['auth']:
    auth.login_required = lambda x: x


# authentication
# --------------
@auth.get_password
def get_password(username):
    """
    Basic authentication. Uses `user` map in config dictionary
    to check passwords.

    :param username: Username to authenticate on.
    """
    if username in config['users']:
        return config['users'][username]
    return None


@auth.error_handler
def unauthorized():
    """
    Deny access to unauthorized user.
    """
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


# error handling
# --------------
@app.errorhandler(400)
def bad_request(error):
    """
    Return response for bad request.
    """
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    """
    Return 404 for missing route.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


# routes
# ------
@app.route('/status', methods=['GET'], endpoint='status')
def status():
    """
    Manage server state.
    """
    return jsonify({'status': 'ok'}), 200


# entrypoint
# ----------
def run():
    app.run(
        host='0.0.0.0',
        debug=config['debug'],
        port=config['port']
    )
    return
