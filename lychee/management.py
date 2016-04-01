import os
import http.server
import socket
import socketserver
import shutil
import sys
from .lychee import build


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "themes")
_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "static")
_POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "posts")


class LycheeTCPServer(socketserver.TCPServer):

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


def generate_structure(path):
    shutil.copytree(_TEMPLATES_DIR, os.path.join(path, 'themes'))
    shutil.copytree(_STATIC_DIR, os.path.join(path, 'static'))
    shutil.copytree(_POSTS_DIR, os.path.join(path, 'posts'))


def execute_from_command_line():
    args = sys.argv[1:]
    if len(args) < 1:
        print('==> error: the command can not understande')
        return
    try:
        if args[0] == 'new' and len(args) == 2:
            path = os.path.join(os.getcwd(), args[1])
            if os.path.exists(path):
                print('=> error: the project is exists')
            else:
                os.mkdir(path)
                generate_structure(path)
                print('=> the project create success')
        elif args[0] == 'serve':
            build(os.getcwd())
            path = os.path.join(os.getcwd(), '_site')
            if not os.path.exists(path):
                print('=> error: the project is not exists')
            os.chdir(path)
            try:
                handler = http.server.SimpleHTTPRequestHandler
                httpd = LycheeTCPServer(('', 4000), handler)
                print('=> now browse to http://localhost:4000')
                httpd.serve_forever()
            except KeyboardInterrupt:
                print('=> stop')
        else:
            print('==> error: the command can not understande')
            return
    except Exception as e:
        print('==> error: some error', e)
