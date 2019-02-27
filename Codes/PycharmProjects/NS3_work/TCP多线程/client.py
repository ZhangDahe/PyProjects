from socket import socket, AF_INET, SOCK_STREAM
import  time
s = socket(AF_INET, SOCK_STREAM)
#s.bind(('127.0.0.1',12345))
s.connect(('localhost', 20000))
s.send('Hello'.encode())
while True:
    a = s.recv(100)
    if a.decode()== 'Hi' :
        s.send('Hello'.encode())
    time.sleep(3)

