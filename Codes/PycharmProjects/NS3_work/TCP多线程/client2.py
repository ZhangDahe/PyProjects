from socket import socket, AF_INET, SOCK_STREAM
import  time
s = socket(AF_INET, SOCK_STREAM)
#s.bind(('127.0.0.1',8888))
s.connect(('localhost', 20000))
s.send('aaaaa'.encode())
while True:
    a = s.recv(100)

    if a.decode()== 'bbbbb' :
        s.send('aaaaa'.encode())
    time.sleep(1)


