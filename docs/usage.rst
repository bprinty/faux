========
Usage
========

The sections below detail different paradigms for using this library. In the documentation below, you'll learn how to use **faux** for: 1) mocking a filesystem during testing, 2) defining a test fixture for mocking an external service, 3) mocking dynamic requests with random data, and 4) pulling mock data from an external service for downstream testing.


Filesystem Mocking
==================

For instance, if you have a directory structure that looks like the following:

.. code-block:: text

    ├── _uuid
    ├── file
    └── query/
        ├── data
        └── arg=test


With the following as contents of the files in that directory structure:

.. code-block:: text

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


You can serve the directory structure using (the `-P` option below is specifying a specific port):

.. code-block:: bash

    ~$ faux serve -P 1234 /path/to/directory


And endpoints mirroring that file structure will be available:

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


It's also worth noting (alluded to above) that you can mock arbitrary data in your responses using methods from the `faker <https://pypi.org/project/Faker/>`_ library. Items like ``{{city}}`` and ``{{month}}`` above were automatically and randomly filled without outputs from a ``faker.Faker()`` object during the request. For more information about the types of data you can fake, see the `faker documentation <https://faker.readthedocs.io/en/master/>`_.

One other special file above is the ``_uuid`` file, which will return data from the ``_uuid`` file whenever a uuid is included as part of the request.



Endpoint Mocking
================

Along with mocking endpoints via filesystem contents, you can also mock endpoints dynamically using the ``faux`` library. Here's and example of how to set up dynamic mocks:

.. code-block:: python

    # imports
    from faux import Server
    
    # set up app
    app = Server(__name__, cache='/path/to/directory')

    # define routes for testing
    @app.route('/simple', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def simple():
        """
        Simple endpint with get/post
        """
        return {
            'status': 'ok',
            'uuid': '{{uuid}}',
            'name': '{{name}}',
            'address': '{{address}}'
        }

    @app.route('/nested/<param>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def nested(param):
        """
        Manage server state.
        """
        return {
            'status': 'ok',
            'param': param,
            'company': '{{company}}',
            'number': '{{random_int}}',
        }

    # run
    if __name__ == '__main__':
        import time
        with app.run(port=1234, debug=True):
            while True:
                time.sleep(1)



Note that ``faux`` uses `Flask <http://flask.pocoo.org/>`_ under the hood to manage endpoint resolution and routing, so the API for this library is very similar to the Flask API. The code above will allow you mock all of the contents of a specified directory, and also the dynamic mocks you've configured with the ``route`` decorator:

.. code-block:: python

    >>> import requests
    >>> r = requests.get('http://localhost:1234/query/data')
    >>> print(r.json())
    {
        "status": "ok",
        "data": "test"
    }
    >>>
    >>> r = requests.get('http://localhost:1234/simple')
    >>> print(r.json())
    {
        "status": "ok",
        "uuid": "4db5fd8c-8aa6-4c29-b979-dab3ce71e64e",
        "name": "Gary Armstrong",
        "address": "97183 Orozco Islands Suite 483\nAndersonton, KS 57080"
    }
    >>>
    >>> r = requests.get('http://localhost:1234/nested/test')
    >>> print(r.json())
    {
        "status": "ok",
        "param": "test",
        "company": "Perez PLC",
        "number": "8032",
    }



Testing Fixtures
================

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


Caching Request Data
====================

Along with serving a directory structure with request data, you can generate that directory structure by querying data from an existing server. For example, if we already had a service that provided the endpoints we tried to mock above, we could query and save that data in a directory structure (for mocking later on) like so:

    >>> from faux import requests
    >>> requests.cache('/path/to/cache/directory')
    >>> requests.get('http://localhost:1234/file')
    >>> requests.get('http://localhost:1234/query?arg=test')
    >>> requests.get('http://localhost:1234/query/data')
    >>> requests.post('http://localhost:1234/query', json={'data': 'test'})


And the contents of our cache directory will look like:

.. code-block:: text

    
    ├── GET/
    │   ├── _uuid
    │   └── query/
    │       ├── data
    │       └── arg=test
    └── POST/
        └── query/
            └── 91cc355


With the files above containing the data from those requests. After generating that cache directory, you can turn around and serve it for testing using ``faux serve`` or using a test fixture.



Command-Line
============

Along with the ``serve`` entrypoint, here is the full set of command-line options available from the `faux` entry-point:

.. code-block:: bash

    ~$ faux -h
    usage: faux [-h] {version,status,serve} ...

    positional arguments:
      {version,status,serve}

    optional arguments:
      -h, --help            show this help message and exit



Starting a Server
-----------------

To start a faux server with an existing directory, you can use the ``serve`` entrypoint: 

.. code-block:: bash

    ~$ faux -h
    usage: faux serve [-h] [-P PORT] [-n NAME] [-t TIMEOUT] [-l LOG_LEVEL] path

    positional arguments:
      path                  Directory structure to serve.

    optional arguments:
      -h, --help            show this help message and exit
      -P PORT, --port PORT  Port to run server on.
      -n NAME, --name NAME  Optional name for server.
      -t TIMEOUT, --timeout TIMEOUT
                            Timeout for stopping server (seconds).
      -l LOG_LEVEL, --log-level LOG_LEVEL
                            Logging verbosity (DEBUG, INFO, ERROR, WARNING,
                            CRITICAL, etc ...). Default is INFO


Example:

.. code-block:: bash

    ~$ faux serve -P 1234 -l INFO -t 100 /path/to/directory



Checking the Status of a Server
-------------------------------

To check the status of a running server, you can use the ``status`` entrypoint:

.. code-block:: bash

    ~$ faux -h
    usage: faux status [-h] [-S] [-H HOST] [-P PORT]

    optional arguments:
      -h, --help            show this help message and exit
      -S, --ssl             Use ssl for connecting to server.
      -H HOST, --host HOST  Host to check.
      -P PORT, --port PORT  Port to check.


Example:

.. code-block:: bash

    ~$ faux status -P 1234
    {'status': 'ok'}


Questions/Feedback
==================

File an issue in the `GitHub issue tracker <https://github.com/bprinty/faux/issues>`_.


