#!/usr/bin/python3

from datetime import datetime
from optparse import OptionParser
from http.server import HTTPServer, BaseHTTPRequestHandler
from .color import Color

g_opt = None

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
    
    def do_POST(self):
        self.print_log()
        self.send_response(200)
        self.end_headers()

def parseOpt():
    parser = OptionParser(usage='%prog [options] [PORT]')
    parser.add_option('-r', '--redirect', dest='redirect', default=None, type=str, help='Redirect')
    parser.add_option('-v', '--verbose', dest='verbose', default=False, action='store_true', help='Verbose')
    parser.add_option('-f', '--file', dest='file', default=None, type=str, help='File')
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        exit(1)
    return options, args

def main():
    global g_opt
    g_opt, args = parseOpt()
    print(f'{Color.green}[*]{Color.reset} Server Start\n')
    server = HTTPServer(('0.0.0.0', int(args[0])), Redirect)
    server.serve_forever()

if __name__ == '__main__':
    main()