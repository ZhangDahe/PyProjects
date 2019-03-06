'''最终版'''
'''新建立一个子线程'''

import socket, threading, time
tcpPort = 8888; checkPeriod = 5; checkTimeout = 10
class Mydict(dict):
    '''管理字典,更新,新建. 返回掉线的client'''
    def __init__(self):
        super(Mydict, self).__init__( )
        """ 创建或更新字典目录"""
    def __setitem__(self, key, value):
        super(Mydict, self).__setitem__(key, value)  # 调用dict中的setitem方法,设置键 和值
    def getSilent(self):
        silent = [ ]
        limit = time.time( ) - checkTimeout  #当前时间 -checkTimeout

        for (ip,ipTime) in self.items():
            if ipTime < limit:
                silent.append(ip)
                break
        return silent

class Receiver(threading.Thread):
    """ 接收tcpp包,并把他们存在字典当中 """
    '''父类 threding.Thread'''
    def __init__(self, mydict):
        super(Receiver, self).__init__( )
        self.mydict = mydict #传入的参数
        self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recSocket.bind(('127.0.0.1', tcpPort))
        self.recSocket.listen(2)

#改写类的run method.`
    def run(self):
        coon, addr = self.recSocket.accept()
        #    try:
        while True:
                data = coon.recv(10)
                print(addr)
                if data.decode() == 'ping':
        #在字典中保存 ip:时间
                    self.mydict[addr[0]] = time.time()
                    print("server is sending 'pang'")
                    coon.send('pang'.encode())

def main():
    mydict = Mydict( )
    receiver = Receiver(mydict=mydict)  # 实例化对象类.
    receiver.start()  # 启动线程


    print ('heartbeat server listening on port %d' % tcpPort)
    while True:
            silent = mydict.getSilent( )
            print ('Silent clients: %s' %silent)
            time.sleep(checkPeriod)
if __name__ == '__main__':
    main( )