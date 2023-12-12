import socket
from sys import platform
import os
import re

def get_ips():
    if platform == "linux":
        cmd = os.popen('ifconfig 2>&-')
        data = cmd.read()
        closeId = cmd.close()
        if closeId != None:
            cmd = os.popen('ip addr 2>&-')
            data = cmd.read()
            closeId = cmd.close()
        if closeId == None:
            return re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', data)
    elif platform == "darwin":
        pass
    return socket.gethostbyname_ex(socket.gethostname())[-1]