# -*- coding: utf-8 -*-
#
# Testing for server caching.
# 
# ------------------------------------------------


# imports
# -------
import os
import json
import unittest
import pytest
from xml.etree import ElementTree

import faux
from faux import requests

from . import config, SANDBOX


# config
# ------
faux.cache(SANDBOX)


# tests
# -----
@pytest.mark.usefixtures("server")
class TestStatic(unittest.TestCase):

    def test_get_root(self):
        # json
        response = requests.get(config.URL + '/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'GET', 'json'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['type'], local['type'])

        # xml
        response = requests.get(config.URL + '/xml')
        self.assertEqual(response.status_code, 200)
        data = ElementTree.fromstring(response.content)
        local = ElementTree.parse(os.path.join(SANDBOX, 'GET', 'xml')).getroot()
        self.assertEqual(data.find('status').text, local.find('status').text)
        self.assertEqual(data.find('type').text, local.find('type').text)

        # text
        response = requests.get(config.URL + '/txt')
        self.assertEqual(response.status_code, 200)
        data = str(response.text.rstrip())
        with open(os.path.join(SANDBOX, 'GET', 'txt'), 'r' ) as fi:
            local = fi.read()
        self.assertEqual(data, local)
        return

    def test_get_query(self):
        # json
        response = requests.get(config.URL + '/query/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'GET', 'query', 'json'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['type'], local['type'])

        # xml
        response = requests.get(config.URL + '/query/xml')
        self.assertEqual(response.status_code, 200)
        data = ElementTree.fromstring(response.content)
        local = ElementTree.parse(os.path.join(SANDBOX, 'GET', 'query', 'xml')).getroot()
        self.assertEqual(data.find('status').text, local.find('status').text)
        self.assertEqual(data.find('type').text, local.find('type').text)

        # text
        response = requests.get(config.URL + '/query/txt')
        self.assertEqual(response.status_code, 200)
        data = str(response.text.rstrip())
        with open(os.path.join(SANDBOX, 'GET', 'query', 'txt'), 'r' ) as fi:
            local = fi.read()
        self.assertEqual(data, local)
        return

    def test_get_params_single(self):
        response = requests.get(config.URL + '?arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'GET', 'arg=test'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        self.assertEqual(data['arg'], local['arg'])
        return

    def test_get_params_multiple(self):
        response = requests.get(config.URL + '?narg=ntest&arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'GET', 'arg=test&narg=ntest'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        self.assertEqual(data['arg'], local['arg'])
        return

    def test_get_query_params_single(self):
        response = requests.get(config.URL + '/query?arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'GET', 'query', 'arg=test'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        self.assertEqual(data['arg'], local['arg'])
        return

    def test_get_query_params_multiple(self):
        response = requests.get(config.URL + '/query?narg=ntest&arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'GET', 'query', 'arg=test&narg=ntest'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        self.assertEqual(data['arg'], local['arg'])
        return

    def test_post_payload(self):
        # test resource: 91cc355
        response = requests.post(config.URL, json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'POST', '91cc355'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        return

    def test_post_params_payload(self):
        # test resource: arg=test91cc355
        response = requests.post(config.URL + '?arg=test', json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'POST', 'arg=test91cc355'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        self.assertEqual(data['arg'], local['arg'])
        return
 
    def test_post_query_payload(self):
        # test resource: query/91cc355
        response = requests.post(config.URL + '/query', json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'POST', 'query', '91cc355'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        return

    def test_post_query_params_payload(self):
        # test resource: query/arg=test91cc355
        response = requests.post(config.URL + '/query?arg=test', json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        with open(os.path.join(SANDBOX, 'POST', 'query', 'arg=test91cc355'), 'r' ) as fi:
            local = json.load(fi)
        self.assertEqual(data['status'], local['status'])
        self.assertEqual(data['param'], local['param'])
        self.assertEqual(data['arg'], local['arg'])
        return

