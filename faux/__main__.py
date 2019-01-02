# -*- coding: utf-8 -*-
#
# Main entry point
#
# ------------------------------------------------


# imports
# -------
import os
import sys
import argparse
import logging

from . import __version__, Server



# args
# ----
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


# version
# -------
parser_version = subparsers.add_parser('version')
parser_version.set_defaults(func=lambda x: sys.stdout.write(__version__ + '\n'))


# status
# ------
def status(args):
    """
    Check if faux server is up and running.
    """
    import requests

    # set up connection params
    url = 'https' if args.ssl else 'http'
    url += '://' + args.host
    if args.port:
        url += ':' + str(args.port)

    # send and parse response
    response = requests.get(url + '/_/status')
    if response.status_code == 200:
        data = response.json()
        if data['status'] != 'ok':
            sys.stderr.write('Could not connect! See `faux serve` for instructions on how to run an instance.\n\n')
            sys.exit(1)
    sys.stdout.write(str(data) + '\n')
    return


parser_status = subparsers.add_parser('status')
parser_status.add_argument('-S', '--ssl', action='store_true', help='Use ssl for connecting to server.', default=False)
parser_status.add_argument('-H', '--host', type=str, help='Host to check.', default='127.0.0.1')
parser_status.add_argument('-P', '--port', type=int, help='Port to check.', default=9001)
parser_status.set_defaults(func=status)


# serve
# ------
def serve(args):
    """
    Run faux server with specified directory structure.
    """
    import time

    # assertions
    if not os.path.exists(args.path):
        raise AssertionError("Error: specified directory to serve does not exist!")

    # set log level
    logging.basicConfig(level=getattr(logging, args.log_level))

    # run server and wait for timeout
    app = Server(__name__, cache=args.path)
    with app.run(port=args.port):
        count = 0
        while True:
            time.sleep(1)
            count += 1
            if args.timeout is None or count > args.timeout:
                break
    return


parser_serve = subparsers.add_parser('serve')
parser_serve.add_argument('-P', '--port', type=int, help='Port to run server on.', default=9001)
parser_serve.add_argument('-n', '--name', type=str, help='Optional name for server.', default=__name__)
parser_serve.add_argument('-t', '--timeout', type=int, help='Timeout for stopping server (seconds).', default=None)
parser_serve.add_argument('-l', '--log-level', help='Logging verbosity (DEBUG, INFO, ERROR, WARNING, CRITICAL, etc ...). Default is INFO', default='INFO')
parser_serve.add_argument('path', help='Directory structure to serve.')
parser_serve.set_defaults(func=serve)


# exec
# ----
def main():
    # parsing
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(0)

    # go!
    args.func(args)
    return


if __name__ == "__main__":
    main()
