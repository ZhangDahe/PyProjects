'''使用socket server module 搭建多线程tcp server'''
'''还没实现'''
from socketserver import BaseRequestHandler, ThreadingTCPServer
import threading,time

BUF_SIZE=10
tcpPort = 12345
checkPeriod = 5
checkTimeout = 20###怎么改,先不管

class Heartbeats(dict):
    """ Manage shared heartbeats dictionary with thread locking """
    '''父类为 dict .管理字典,更新,新建. 返回掉线的client'''
    #super,调用父类进行初始化.http://funhacks.net/explore-python/Class/super.html
    def __init__(self):
        super(Heartbeats, self).__init__( )
        self._lock = threading.Lock( )  # 初始化一个锁对象,一个线程得到锁了,其他的线程都会被阻塞.直到锁被释放.
    def __setitem__(self, key, value):
        """ Create or update the dictionary entry for a client 创造或更新字典目录"""
        self._lock.acquire( )      #获得锁.
        try:
            super(Heartbeats, self).__setitem__(key, value)  #调用dict中的setitem方法,设置键 和值
        finally:
            self._lock.release( ) #释放锁
    def getSilent(self):
        """ 返回掉线的client.Return a list of clie  nts with heartbeat older than CHECK_TIMEOUT """
        limit = time.time( ) - checkTimeout  #当前时间 -checkTimeout
        self._lock.acquire( )
        try:
            silent = [ip for (ip, ipTime) in self.items( ) if ipTime < limit]
        finally:
            self._lock.release( )
        return silent

'1 集成baserequesthandler,重写handle method'


class MyTcpHandler(BaseRequestHandler):
    '''处理request 的函数'''

    '''in handle method.For stream services, self.request is a socket object;'''
    def __init__(self,heatbeats):  ##只是警告好嘛,不用担心的
        super(BaseRequestHandler,self).__init__()
        self.heartbeats = heartbeats

    def handle(self):
        addr = self.client_address
        print('%s connected!' %addr)
        while True:
            data = self.request.recv(BUF_SIZE)
            if  data.decode() == 'ping':

                cur_thread = threading.current_thread()
                print(cur_thread)

                self.heartbeats[addr[0]] = time.time()
                self.request.sendall('pang'.encode('utf-8'))

            else:
                print('close')
                break

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 12345
    ADDR = (HOST, PORT)

    heartbeats = Heartbeats()  # 实例化 字典类
    #为啥要用with???
    with  ThreadingTCPServer(ADDR, MyTcpHandler) as server :
             server.serve_forever()  #监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理

    try:
        while True:
                  silent = heartbeats.getSilent()
                  print('Silent clients: %s' % silent)
                  time.sleep(checkPeriod)
    except KeyboardInterrupt:
        print ('Exiting, please wait...')
