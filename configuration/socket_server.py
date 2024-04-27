import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 8888

s.bind((host, port))
s.listen(5)

while True:
    c, addr = s.accept()
    print("Connected to %s" % addr)
    c.send("superhash")
    c.close() 