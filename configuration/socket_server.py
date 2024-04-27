import socket
from mininet.log import setLogLevel, info
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
setLogLevel("info")
host = '127.0.0.1'
port = 8888

s.bind((host, port))
s.listen(5)
info("Server up \n")
while True:
    c, addr = s.accept()
    print("Connected to %s" % addr)
    c.send("superhash")
    c.close() 