from heapq import  heappush,heappop     #引入堆模块
import queue                            #队列
import numpy

'''服务窗口，参数 ：total_servicetime,beta,mu'''

class service_window:
    def __init__(self, total_servicetime, beta, mu):
        self.total_servicetime = total_servicetime
        self.labda = 1/beta  # beta =  1/lambta.
        self.mu = mu

        self.time = 0  # 仿真系统中的时刻
        self.user_queue = queue.Queue()  # 存user的队列
        self.event_queue = [ ]  #  存事件的list
        self.record = recorder() # 实例化类recorder（），
        self.user_beserved = None  #？？？

    '''记录系统的状态，需要一个时间。就像拍照，每隔多久拍一次照片。monitorstartingtime 就是 第一次拍照的时刻'''
    def start_sim(self,first_record_time):

        self.first_record_time = first_record_time

        #初始化第一个用户到达事件和monitor 事件。放入堆中
        heappush(self.event_queue, (numpy.random.exponential(self.labda), "arrive"))
        heappush(self.event_queue, (first_record_time, "Monitor"))


        '''写的时候，应该用while而不是if。死循环，不停的去检测 顶端的事件,然后调用 handle_event函数去处理。事件驱动的关键点在此'''
        while self.time < self.total_servicetime:
              a = heappop(self.event_queue)
              self.time = a[0]
              self.handle_event(a[1])

    def handle_event(self, event):

        if event == "arrive":
            next_user_arrive_time = self.time + numpy.random.exponential(self.labda)
            next_user = User(next_user_arrive_time)

            heappush(self.event_queue, (next_user_arrive_time, "arrive"))
            self.user_queue.put(next_user)

            # 服务当前的user
            if self.user_beserved == None  and not self.user_queue.empty():
                user = self.user_queue.get()
                self.user_beserved = user

                left_time = self.time + numpy.random.exponential(self.mu)
                heappush(self.event_queue, (left_time, "left"))

        elif event == "left":

            self.user_beserved.set_left_time(self.time)
            last_left = self.user_beserved
            self.user_beserved = None

            #若目前 时间已经越过了第一次采集的时间，那就记录信息
            #保证了程序的严谨性，没有其他用途。
            if self.time >self.first_record_time :
                 self.record.record_stay_time(last_left)
            #window 空闲，则服务下一个user
            if not self.user_queue.empty():
                  a = self.user_queue.get()
                  self.user_beserved = a

                  left_time = self.time + numpy.random.exponential(self.mu)
                  heappush(self.event_queue, (left_time, "left"))
        else:
            user_waiting = self.user_queue.qsize()
            self.record.record_usernum(user_waiting)
            next_record_time = self.time + numpy.random.exponential(self.labda/2)
            heappush(self.event_queue,(next_record_time,"Monitor"))
            #set next  record event
            #what if i dont set it?
class User:
    def __init__(self, arrive_time):
        self.arrive_time = arrive_time

    def set_left_time(self, left_time):
        self.left_time = left_time

    def get_staytime(self):
        return self.left_time - self.arrive_time

class recorder():
    def __init__(self):
        self.cnt = 0  # 计数 recorder 的运行次数
        self.user_waiting = []  # 用列表形式，存储每一次进入recorder时
        # 系统中的等待user数量。 达到平均的排队人数
        #系统总共服务了多少个user
        self.user_num = 0
        self.stay_time = [ ] # 用列表形式 记录每个人的等待时间，最后求和取平均
    # 记录用户数，每个用户从到达 到离去经过的时长。
    def record_stay_time(self, user):
        self.user_num += 1
        self.stay_time.append(user.get_staytime())
    # 记录每次统计时的等待用户数，以及记录了多少次，最后好取平均用。
    def record_usernum(self, user_waiting):
        self.cnt += 1
        self.user_waiting.append(user_waiting)
    def print_record(self):
        print("Average Waiting Requests: " + str(sum(self.user_waiting) / self.cnt))
        print("Average Stay Time : " + str(sum(self.stay_time) / self.user_num))


#------------------------------- main ---------------------------------------
print("lambda =50  , mu = 2")
mm1 = service_window(400,50,0.015)
mm1.start_sim(100)
mm1.record.print_record()