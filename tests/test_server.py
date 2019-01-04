# -*- coding: utf-8 -*-
#
# Testing for server caching.
# 
# ------------------------------------------------


# imports
# -------
import unittest
import pytest
import requests
from xml.etree import ElementTree
from . import config


# tests
# -----
@pytest.mark.usefixtures("server")
class TestLocalMock(unittest.TestCase):

    def test_no_file(self):
        response = requests.get(config.URL + '/missing')
        self.assertEqual(response.status_code, 404)
        return

    def test_status(self):
        response = requests.get(config.URL + '/_/status')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        return
    
    def test_get_root(self):
        # json
        response = requests.get(config.URL + '/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['type'], 'json')

        # xml
        response = requests.get(config.URL + '/xml')
        self.assertEqual(response.status_code, 200)
        data = ElementTree.fromstring(response.content)
        self.assertEqual(data.find('status').text, 'ok')
        self.assertEqual(data.find('type').text, 'xml')

        # text
        response = requests.get(config.URL + '/txt')
        self.assertEqual(response.status_code, 200)
        data = str(response.text.rstrip())
        self.assertEqual(data, 'test')
        return

    def test_get_query(self):
        # json
        response = requests.get(config.URL + '/query/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['type'], 'json')

        # xml
        response = requests.get(config.URL + '/query/xml')
        self.assertEqual(response.status_code, 200)
        data = ElementTree.fromstring(response.content)
        self.assertEqual(data.find('status').text, 'ok')
        self.assertEqual(data.find('type').text, 'xml')

        # text
        response = requests.get(config.URL + '/query/txt')
        self.assertEqual(response.status_code, 200)
        data = str(response.text.rstrip())
        self.assertEqual(data, 'test')
        return

    def test_get_params_single(self):
        response = requests.get(config.URL + '?arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['arg'], 'test')
        return

    def test_get_params_multiple(self):
        response = requests.get(config.URL + '?narg=ntest&arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['arg'], 'test')
        return

    def test_get_query_params_single(self):
        response = requests.get(config.URL + '/query?arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['arg'], 'test')
        return

    def test_get_query_params_multiple(self):
        response = requests.get(config.URL + '/query?narg=ntest&arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['arg'], 'test')
        return

    def test_post_payload(self):
        # test resource: 1906fde
        response = requests.post(config.URL, json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        return

    def test_post_params_payload(self):
        # test resource: arg=test1906fde
        response = requests.post(config.URL + '?arg=test', json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['arg'], 'test')
        return
 
    def test_post_query_payload(self):
        # test resource: query/1906fde
        response = requests.post(config.URL + '/query', json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        return

    def test_post_query_params_payload(self):
        # test resource: query/arg=test1906fde
        response = requests.post(config.URL + '/query?arg=test', json={'data': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['arg'], 'test')
        return

    def test_get_named_param(self):
        import uuid
        uu = str(uuid.uuid4())

        # root
        response = requests.get(config.URL + '/' + uu)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertTrue('uuid' in data)

        # query
        response = requests.get(config.URL + '/query/' + uu)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertTrue('uuid' in data)
        return

    def test_resolve_with_post_method(self):
        # GET
        response = requests.get(config.URL + '/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['type'], 'json')

        # POST
        response = requests.post(config.URL + '/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['type'], 'json')

        # PUT
        response = requests.put(config.URL + '/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['type'], 'json')
        return



@pytest.mark.usefixtures("server")
class TestDynamicMock(unittest.TestCase):

    # GET
    def test_get_simple(self):
        response = requests.get(config.URL + '/simple')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        return 

    def test_get_simple_args(self):
        response = requests.get(config.URL + '/simple?arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['arg'], 'test')
        return

    def test_get_nested(self):
        response = requests.get(config.URL + '/nested/test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        return

    def test_get_nested_args(self):
        response = requests.get(config.URL + '/nested/test?arg=test')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['arg'], 'test')
        return

    # POST
    def test_post_simple(self):
        response = requests.post(config.URL + '/simple', json={'param': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        return

    def test_post_simple_args(self):
        response = requests.post(config.URL + '/simple?arg=test', json={'param': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['arg'], 'test')
        self.assertEqual(data['param'], 'test')
        return

    def test_post_nested(self):
        response = requests.post(config.URL + '/nested/test', json={'payload': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['payload'], 'test')
        return

    def test_post_nested_args(self):
        response = requests.post(config.URL + '/nested/test?arg=test', json={'payload': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['arg'], 'test')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['payload'], 'test')
        return

    # PUT
    def test_put_simple(self):
        response = requests.put(config.URL + '/simple', json={'param': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        return

    def test_put_simple_args(self):
        response = requests.put(config.URL + '/simple?arg=test', json={'param': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['arg'], 'test')
        self.assertEqual(data['param'], 'test')
        return

    def test_put_nested(self):
        response = requests.put(config.URL + '/nested/test', json={'payload': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['payload'], 'test')
        return

    def test_put_nested_args(self):
        response = requests.put(config.URL + '/nested/test?arg=test', json={'payload': 'test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['arg'], 'test')
        self.assertEqual(data['param'], 'test')
        self.assertEqual(data['payload'], 'test')
        return
