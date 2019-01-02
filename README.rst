Faux
====

Quick and easy server mocking.


Installation
------------

Via github:

.. code-block:: bash

    ~$ git clone http://github.com/bprinty/faux.git
    ~$ cd faux
    ~$ python setup.py install


Via pip:

.. code-block:: bash

    ~$ pip install faux


Documentation
-------------

Documentation for the package can be found `here <http://faux.readthedocs.io/en/latest/index.html>`_.


Usage
-----

The `faux <http://github.com/bprinty/faux>`_ provides utilities for mocking responses from external services during testing. With `faux`, you can easily serve a directory structure mocking url endpoints for an externally managed service and use that server for testing.


High-Level
++++++++++

For instance, if you have a directory structure that looks like the following:

.. code-block::

    ├── _uuid
    ├── file
    └── query/
        ├── data
        └── arg=test


With the following as contents of the files in that directory structure:

.. code-block::

    # _uuid
    {
        "status": "ok",
        "city": "{{city}}"
    }

    # file
    {
        "status": "ok",
        "month": "{{month}}",
    }

    # query/arg=test
    {
        "status": "ok",
        "arg": "test",
        "digit": {{random_digit}}
    }

    # query/data
    {
        "status": "ok",
        "data": "test"
    }


Endpoints mirroring that file structure will be available:

.. code-block:: python

    >>> import requests
    >>> r = requests.get('http://localhost:1234/4db5fd8c-8aa6-4c29-b979-dab3ce71e64e')
    >>> print(r.json())
    {
        "status": "ok",
        "city": "Sacramento",
    }

    >>> r = requests.get('http://localhost:1234/file')
    >>> print(r.json())
    {
        "status": "ok",
        "month": "05"
    }

    >>> r = requests.get('http://localhost:1234/query?arg=test')
    >>> print(r.json())
    {
        "status": "ok",
        "arg": "test",
        "digit": 4
    }

    >>> r = requests.get('http://localhost:1234/query/data')
    >>> print(r.json())
    {
        "status": "ok",
        "data": "test"
    }


It's also worth noting (alluded to above) that you can mock arbitrary data in your responses using methods from the `faker <https://pypi.org/project/Faker/>`_ library. Items like `{{city}}` and `{{month}}` above were automatically and randomly filled without outputs from a `faker.Faker()` object during the request.

One other special file above is the `_uuid` file, which will return data from the `_uuid` file whenever a uuid is included as part of the request.



Starting a Server
+++++++++++++++++

For the previous example, you can start the server on a specific port using::

.. code-block:: bash

    ~$ faux serve -P 1234 /path/to/directory



Using Within Tests
++++++++++++++++++

One of the most common paradigms for using this software is to mock a service during testing. To do so with this module, you can easily set up a py.test fixture that will run throughout your test session:

.. code-block:: python

    import unittest
    import pytest
        
    RESOURCES = '/path/to/testing/resources'

    @pytest.fixture(scope='session')
    def server():
        """
        Set up mock server for testing request caching.
        """
        from faux import Server
        app = Server(__name__, cache=RESOURCES)
        with app.run(port=1234):
            yield
        return


Once you've defined the fixture, you can use it on a test class or function like so:

.. code-block:: python

    # test function
    @pytest.mark.usefixtures("server")
    def test_function():
        return


    # test class
    @pytest.mark.usefixtures("server")
    class TestClass(unittest.TestCase):
        def test_method():
            return


With the code above, the server you're mocking will run throughout your testing session and will gracefully exit when the test session stops.


Other Functionality
+++++++++++++++++++

To see other functionality provided by the library, please see the `documentation <http://faux.readthedocs.io/en/latest/index.html>`_.


Questions/Feedback
------------------

File an issue in the `GitHub issue tracker <https://github.com/bprinty/faux/issues>`_.

