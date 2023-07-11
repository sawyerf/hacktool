import socket

def get_ips():
    return socket.gethostbyname_ex(socket.gethostname())[-1]