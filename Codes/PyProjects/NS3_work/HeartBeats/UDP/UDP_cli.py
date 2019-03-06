'''udp  client '''
'''向 server 每隔5s  发一个'ping' '''
import socket, time
serverIp = '127.0.0.1'; serverPort =9999; sendPeriod = 1
print ('Sending heartbeat package to IP %s , port %d' % (serverIp,serverPort))

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto('ping'.encode(), (serverIp, serverPort))

    data,addr = s.recvfrom(5)
    if data.decode() == 'pang' :
        print('Time: %s' % time.ctime())
        time.sleep(sendPeriod)