import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = sys.argv[0]
port = 8888

s.connect((host, port))
print(s.recv(1024))

s.close()