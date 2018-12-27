# -*- coding: utf-8 -*-
#
# Testing for server caching.
# 
# ------------------------------------------------


# imports
# -------
import unittest
import pytest
from smock import smock



# config
# ------
@pytest.fixture(autouse=True, scope='session')
def serve():
    from . import RESOURCES
    with smock.run(port=PORT, cache=RESOURCES):
        yield
    return



# tests
# -----
class TestStatic(unittest.TestCase):

    def test_static_file(self):
        return

