========
Usage
========




.. code-block:: python

    # imports
    from smock import Server
    
    # set up app
    app = Server(__name__, cache='resources')

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
        app.run(
            port=1234,
            debug=True
        )



.. code-block:: python

    >>> import requests
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
        "number": 8032,
    }



.. code-block::

    ├── _uuid
    ├── file
    └── query/
        ├── data
        └── arg=test



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



.. code-block:: python

    import pytest

    @pytest.fixture(scope='session')
    def server():
        """
        Set up mock server for testing request caching.
        """
        from smock import Server
        app = Server(__name__, cache='resources')
        with app.run(port=1234):
            yield
        return


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
