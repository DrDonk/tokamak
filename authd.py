import struct
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target = '127.0.0.1'
port = 902
s.connect((target, port))
data = s.recv(1024)
s.send('USER dave\r\n')
data = s.recv(1024)
s.send('PASS kalkan7& \r\n')
data = s.recv(1024)
s.close()
