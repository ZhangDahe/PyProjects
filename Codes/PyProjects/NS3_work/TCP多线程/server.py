from socketserver import BaseRequestHandler, ThreadingTCPServer
import  threading

class EchoHandler(BaseRequestHandler):
    '''多个线程只能使用 同一个handler函数？？如果想给不同的线程分配不同的handler
    怎么办？ 在数据中标识区分出不同的client?
    '''
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            cur_thread = threading.current_thread()
            print(cur_thread)
            msg = self.request.recv(100)
            print(msg.decode())
            if   msg.decode() == 'Hello' :
                self.request.send('Hi'.encode())
            elif msg.decode() == 'aaaaa':
                self.request.send('bbbbb'.encode())


if __name__ == '__main__':
     with ThreadingTCPServer(('', 20000), EchoHandler) as serv:
       serv.serve_forever()