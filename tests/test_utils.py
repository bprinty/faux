# -*- coding: utf-8 -*-
#
# Testing for server caching.
# 
# ------------------------------------------------


# imports
# -------
import unittest
import pytest
from faux.utils import format_data
import json


# tests
# -----
class TestFormatData(unittest.TestCase):

    def test_json(self):
        data = {
            'uuid': 'a{{uuid}}asdf',
            'name': '{{name }}aasdf',
            'text': 'basfg{{ text}}',
            'address': 'asdf{{ address }}asdf',
            'none': 'name'
        }
        res = json.loads(format_data(json.dumps(data)), strict=False)
        self.assertNotEqual(res['uuid'], data['uuid'])
        self.assertNotEqual(res['name'], data['name'])
        self.assertNotEqual(res['text'], data['name'])
        self.assertNotEqual(res['address'], data['address'])
        self.assertEqual(res['none'], data['none'])
        return

    def test_xml(self):
        # TODO: THIS
        return

