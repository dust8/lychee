import os
import argparse
import sys
import http.server
import socketserver
from .lychee import generate_structure, build


def parse_args():
    parser = argparse.ArgumentParser(
        description='Transform your plain text into static blogs.')
    parser.add_argument('-new', help='new')
    parser.add_argument('-build', help='build')
    parser.add_argument('-serve', help='serve')

    args = parser.parse_args()
    return args


def execute_from_command_line(argv=None):
    args = parse_args()

    if args.new:
        path = os.path.join(os.getcwd(), args.new)
        if os.path.exists(path):
            print('=> error: the project is exists!')
        else:
            os.mkdir(path)
            generate_structure(path)
            print('=> the project create success!')

    if args.build:
        path = os.path.join(os.getcwd(), args.build)
        build(path)

    if args.serve:
        path = os.path.join(os.getcwd(), args.serve)
        if not os.path.exists(path):
            print('=> error: the project is not exissts!')
        os.chdir(path)
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(('', 4000), handler)
        print('=> now browse to http://localhost:4000')
        httpd.serve_forever()

