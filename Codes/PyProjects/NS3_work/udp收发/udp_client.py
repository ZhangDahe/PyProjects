import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto('PyHB'.encode(),('127.0.0.1',9999))
#把str转化为 bytes发送.
s.close()