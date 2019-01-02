# -*- coding: utf-8 -*-
#
# testing for entry points
#
# ------------------------------------------------


# imports
# -------
import os
import unittest
import pytest
import subprocess
import time
import json
import ast
import requests

from faux import __version__
from faux import __main__ as cli
from faux.utils import free_port

from . import RESOURCES, SANDBOX, ROOT


# tests
# -----
class TestEntryPoints(unittest.TestCase):

    def call(self, subcommand, *args):
        return subprocess.check_output('PYTHONPATH=$PYTHONPATH:{} python -m faux {} {}'.format(
            ROOT, subcommand, ' '.join(args)
        ), stderr=subprocess.STDOUT, shell=True)

    def popen(self, subcommand, *args):
        return subprocess.Popen('PYTHONPATH=$PYTHONPATH:{} python -m faux {} {}'.format(
            ROOT, subcommand, ' '.join(args)
        ), stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)

    def test_version(self):
        res = self.call('version').decode('utf-8')
        self.assertEqual(__version__, res.rstrip())
        return

    def test_serve_status(self):
        # start server with 3 second timeout
        port = str(free_port())
        self.popen('serve', '-t', '3', '-P', port, RESOURCES)
        time.sleep(1)
        
        # query status
        res = self.call('status', '-P', port).decode('utf-8')
        data = ast.literal_eval(res) # not sure why json.loads doesn't work here.
        self.assertEqual(data['status'], 'ok')

        # test with request
        result = requests.get('http://127.0.0.1:{}/json'.format(port))
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()['status'], 'ok')
        return
