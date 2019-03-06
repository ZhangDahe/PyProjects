
'''初探 from  廖雪峰'''
import time, threading
# 新线程执行的代码:
def loop():

    print('thread %s is running...' % threading.current_thread().name) # 2.thread LoopThread is running...

    n = 0
    while n < 5:
        n += 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

#===============================================================================#

print('thread %s is running...' % threading.current_thread().name)  # 打印的效果 1. thread MainThread is running...

t = threading.Thread(target=loop, name='LoopThread')  # name 填的是 线程名称,新建一个线程. LoopThread
t.start()
t.join() #等待子线程结束之后,主线程才会结束.
print('thread %s ended.' % threading.current_thread().name)