import socket
import sys
from mininet.log import setLogLevel, info

setLogLevel("info")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[0]
port = 8888

s.connect((host, port))
info("Client connected \n")
print(s.recv(1024))

s.close()