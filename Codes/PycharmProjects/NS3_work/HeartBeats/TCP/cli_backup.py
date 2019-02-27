

'''向 server 每隔5s  发一个'ping'   tcp连接 '''
import socket, time
serverIp = '127.0.0.1'; serverPort =12345; sendPeriod = 5
print ('Sending heartbeat package to IP %s , port %d' % (serverIp,serverPort))
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('127.0.0.1', 10011))
# s.connect((serverIp, serverPort))

#s.bind(('127.0.0.1', 10009))

while True:
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((serverIp, serverPort))
     s.send('ping'.encode())

    # print(data.decode())
     data = s.recv(5)
     if data.decode('utf-8') == 'pang' :
        print('Time: %s' %time.ctime())
        time.sleep(sendPeriod)

