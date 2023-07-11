from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import requests
import socket

from .color import Color
from .ip import get_ips

links = {
    'deepce.sh': 'https://github.com/stealthcopter/deepce/raw/main/deepce.sh',
    'linpeas.sh': 'https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh',
    'lse.sh': 'https://github.com/diego-treitos/linux-smart-enumeration/raw/master/lse.sh',
    'ncat': 'https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/ncat',
    'nmap': 'https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/nmap',
    'pspy32': 'https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy32',
    'pspy64': 'https://github.com/DominicBreuker/pspy/releases/download/v1.2.1/pspy64',
    'winpeas.exe': 'https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEASany.exe',
}

class Redirect(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def index_page(self, urls):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<ul>\n')
        for url in urls:
            self.wfile.write(f'<li><a href="/{url}">{url}</a></li>\n'.encode())
        self.wfile.write(b'</ul>')

    def do_GET(self):
        if self.path[1:] in links:
            r = requests.get(links[self.path[1:]])
            if r.status_code == 200:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(r.content)
            else:
                self.send_response(r.status_code)
                self.end_headers()
        elif self.path == '/linux':
            self.index_page(['linpeas.sh', 'lse.sh', 'deepce.sh', 'ncat', 'nmap', 'pspy64'])
        elif self.path == '/base':
            self.index_page(['linpeas.sh', 'pspy64'])
        elif self.path == '/win':
            self.index_page(['winpeas.exe'])
        elif self.path == '/':
            self.index_page(links.keys())
        else:
            self.send_response(404)
            self.end_headers()

def parseOpt():
    parser = OptionParser(usage='%prog [options] [PORT]')
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        exit(1)
    return options, args


def main():
    global g_opt
    g_opt, args = parseOpt()

    print(f'{Color.yellow}==============={Color.reset}')
    print(f'{Color.red}IP:{Color.reset}')
    ips = get_ips()
    for ip in ips:
        print(f'       {ip}')
    print(f'{Color.yellow}==============={Color.reset}')
    print(f'{Color.red}LINK:{Color.reset}')
    ip = ''
    if len(ips) == 1:
        ip = ips[0]
    print(f'       http://{ip}:{args[0]}/')
    for script in links:
        print(f'       http://{ip}:{args[0]}/{script}')
    print(f'{Color.red}BUNDLE:{Color.reset}')
    for bundle in ['base', 'linux', 'win']:
        print(f'       http://{ip}:{args[0]}/{bundle}')
    print(f'{Color.yellow}==============={Color.reset}')
    print()
    print(f'{Color.green}[*]{Color.reset} Server Start\n')

    server = HTTPServer(('0.0.0.0', int(args[0])), Redirect)
    server.serve_forever()

if __name__ == '__main__':
    main()