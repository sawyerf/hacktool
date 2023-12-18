#!/usr/bin/python3

from datetime import datetime
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import BaseCookie,SimpleCookie
import urllib.parse
import base64
import re
from .color import Color
from .ip import get_ips
import os

g_opt = None

def decode_data(data):
    # urlencode
    if '%' in data:
        try:
            return decode_data(urllib.parse.unquote(data))
        except:
            pass
    # base64
    if re.match(r'^[a-zA-Z0-9+/]+={0,2}$', data):
        try:
            return decode_data(base64.b64decode(data, validate=False).decode())
        except:
            pass
    # jwt
    if re.match(r'^[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$', data):
        try:
            jwt_data = data.split('.')[1]
            jwt_data += '=' * (4 - len(jwt_data) % 4)
            return decode_data(base64.b64decode(jwt_data).decode())
        except:
            pass
    return data

class Redirect(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        if g_opt.file:
            with open(g_opt.file, 'rb') as f:
                self.file_data = f.read()
        super().__init__(*args, **kwargs)

    def log_message(self, format, *args):
        pass

    def print_log(self):
        date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        print(f'{Color.green}[{date}] {Color.reset}{self.client_address[0]} - {Color.red}{self.command} {self.path}{Color.reset}')
        if g_opt.verbose:
            print(self.requestline)
            print(self.headers)
            if 'Content-Length' in self.headers:
                print(f'{Color.yellow}', end='')
                post_data = self.rfile.read(int(self.headers['Content-Length']))
                print(post_data.decode('utf-8', errors='ignore'))
                print(f'{Color.reset}', end='')
            self.decode()

    def decode(self):
        url = urllib.parse.urlparse(self.path)
        if '%' not in url.path and 'Cookie' not in self.headers and not url.query:
            return
        print(f'{Color.pink}======= DECODED ======={Color.reset}')
        if '%' in url.path:
            print(f'{Color.pink}Path:{Color.reset}')
            print(urllib.parse.unquote(url.path))
        if url.query:
            print(f'{Color.pink}Query:{Color.reset}')
            query = urllib.parse.parse_qs(url.query, keep_blank_values=True, errors='ignore')
            for key, value in query.items():
                print(f'{key}: {decode_data(value[0])}')
        if 'Cookie' in self.headers:
            print(f'{Color.pink}Cookie:{Color.reset}')
            cookie = SimpleCookie()
            cookie.load(self.headers['Cookie'])
            for key, value in cookie.items():
                print(f'{key}: {decode_data(value.value)}')
        print(f'')

    def do_GET(self):
        self.print_log()
        if g_opt.redirect:
            self.send_response(301)
            self.send_header('Location', g_opt.redirect)
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            if g_opt.file:
                self.wfile.write(self.file_data)
            elif g_opt.explorer:
                path = g_opt.explorer + self.path
                # if folder
                if os.path.isdir(path):
                    self.wfile.write(b'<html><body>')
                    for f in os.listdir(path):
                        self.wfile.write(f'<a href="{f}">{f}</a><br>'.encode())
                    self.wfile.write(b'</body></html>')
                elif os.path.isfile(path):
                    with open(path, 'rb') as f:
                        self.wfile.write(f.read())
    
    def do_POST(self):
        self.print_log()
        self.send_response(200)
        self.end_headers()

def parseOpt():
    parser = OptionParser(usage='%prog [options] [PORT]')
    parser.add_option('-e', '--explorer', dest='explorer', default=None, type=str, help='Send file of the current folder')
    parser.add_option('-f', '--file', dest='file', default=None, type=str, help='File')
    parser.add_option('-r', '--redirect', dest='redirect', default=None, type=str, help='Redirect')
    parser.add_option('-v', '--verbose', dest='verbose', default=True, action='store_false', help='Disable verbose')
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        exit(1)
    if options.explorer and options.file:
        print('[-] -f and -e cannot be used at the same time')
        parser.print_help()
        exit(1)
    return options, args

def main():
    global g_opt
    g_opt, args = parseOpt()
    print(f'{Color.yellow}==============={Color.reset}')
    print(f'{Color.red}LINK:{Color.reset}')
    ips = get_ips()
    for ip in ips:
        print(f'       http://{ip}:{args[0]}/')
    print(f'{Color.yellow}==============={Color.reset}')
    print(f'{Color.green}[*]{Color.reset} Server Start\n')
    server = HTTPServer(('0.0.0.0', int(args[0])), Redirect)
    server.serve_forever()

if __name__ == '__main__':
    main()