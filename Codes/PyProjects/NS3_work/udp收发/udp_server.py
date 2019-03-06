import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1',9999))

print('-----Listen udp: 9999 ------')
while True:
    data,addr=s.recvfrom(1024)
    print(addr)

    #收到的是bytes数据.
    print(data)
    print((data.decode()))