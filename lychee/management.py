import os
import argparse
import sys
import http.server
import socketserver
import shutil
from .lychee import build


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "templates")
_POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "posts")
_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "static")

def parse_args():
    parser = argparse.ArgumentParser(
        description='Transform your plain text into static blogs.')
    parser.add_argument('-new', help='new')
    parser.add_argument('-build', help='build')
    parser.add_argument('-serve', help='serve')

    args = parser.parse_args()
    return args

def generate_structure(path):
    shutil.copytree(_TEMPLATES_DIR, os.path.join(path, 'templates'))
    shutil.copytree(_POSTS_DIR, os.path.join(path, 'posts'))
    shutil.copytree(_STATIC_DIR, os.path.join(path, 'static'))

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
            print('=> error: the project is not exists!')
        os.chdir(path)
        try:
            handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(('', 4000), handler)
            print('=> now browse to http://localhost:4000')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('=> stop')
