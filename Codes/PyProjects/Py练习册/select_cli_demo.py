# coding: utf-8
import socket




server_address = ('localhost', 8090)

# Create aTCP/IP socket
#居然搞了两个套接字
socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM), socket.socket(socket.AF_INET,  socket.SOCK_STREAM)]

# 连接到服务器
for s in socks:
    s.connect(server_address)


messages = ['This is the message ', 'It will be sent ', 'in parts ', ]
for index, message in enumerate(messages):
    # Send messages on both sockets
    for s in socks:
        print ('%s: sending "%s"' % (s.getsockname(), message + str(index)))
    #    s.send((message + str(index)).encode('utf-8'))
        s.send(message.encode('utf-8'))
    # Read responses on both sockets

for s in socks:
    data = s.recv(1024)
    print ('%s: received "%s"' % (s.getsockname(), data))
    if data != "":
        print ('closingsocket', s.getsockname())
        s.close()