
'''udp server'''

'''多线程操作'''

import socket, threading, time
UDP_PORT = 43278; CHECK_PERIOD = 20; CHECK_TIMEOUT = 15
class Heartbeats(dict):
    """ Manage shared heartbeats dictionary with thread locking """
    '''管理字典,更新,新建. 返回掉线的client'''
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
        """ 返回掉线的client.Return a list of clients with heartbeat older than CHECK_TIMEOUT """
        limit = time.time( ) - CHECK_TIMEOUT  #当前时间 -check_timeout
        self._lock.acquire( )
        try:
            silent = [ip for (ip, ipTime) in self.items( ) if ipTime < limit]
        finally:
            self._lock.release( )
        return silent

class Receiver(threading.Thread):
    """ 接收udp包,并把他们存在字典当中.Receive UDP packets and log them in the heartbeats dictionary """
    '''父类 threding.Thread'''
    def __init__(self, goOnEvent, heartbeats):
        super(Receiver, self).__init__( )

        self.goOnEvent = goOnEvent
        self.heartbeats = heartbeats #传入的参数

        self.recSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recSocket.settimeout(CHECK_TIMEOUT)
        self.recSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recSocket.bind(('127.0.0.1', UDP_PORT))

#改写类的run method.
    def run(self):
        while self.goOnEvent.isSet( ):#当标志为true时
            try:
                data, addr = self.recSocket.recvfrom(5)
                if data == 'PyHB':
                    #在字典中保存 ip:时间
                    self.heartbeats[addr[0]] = time.time( )
            except socket.timeout:
                pass

def main(num_receivers=3):

    receiverEvent = threading.Event( )
    receiverEvent.set( )
    #设标志为 true

    #实例化对象  heartbeats
    heartbeats = Heartbeats( )
    receivers = [ ]


    for i in range(num_receivers):

        receiver = Receiver(goOnEvent=receiverEvent, heartbeats=heartbeats)  #实例化对象.
        receivers.append(receiver)  # 将线程添加到线程列表
        receiver.start( ) #启动线程


    print ('Threaded heartbeat server listening on port %d' % UDP_PORT)
    print ('press Ctrl-C to stop')
    try:
        while True:
            silent = heartbeats.getSilent( )
            print ('Silent clients: %s' % silent)
            time.sleep(CHECK_PERIOD)

    #一旦有键盘中断时,进行清理.
    except KeyboardInterrupt:
        print ('Exiting, please wait...')
        receiverEvent.clear( )
        for receiver in receivers:
            receiver.join( )
        print ('Finished.')
if __name__ == '__main__':
    main( )