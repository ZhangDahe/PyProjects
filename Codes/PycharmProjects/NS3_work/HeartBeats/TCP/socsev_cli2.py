'''tcp最终版本,未实现多个客户端'''
'''向 server 每隔2s  发一个'ping'   tcp连接 '''
import socket, time
def main():
    serverIp = '127.0.0.1'; serverPort =8888; sendPeriod = 2
    print ('Sending heartbeat package to IP %s , port %d' % (serverIp,serverPort))
    aa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    aa.bind(('127.0.0.1', 18888))
    aa.connect((serverIp, serverPort))
    aa.send('ping'.encode())

    while True:
  #   print('i')
      data = aa.recv(10)
      if data.decode('utf-8') == 'pang' :
          aa.send('ping'.encode())
          print('Time: %s' %time.ctime())
          time.sleep(sendPeriod)


if __name__ == '__main__':
    main()
