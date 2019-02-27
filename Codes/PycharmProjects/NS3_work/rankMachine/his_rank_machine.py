from __future__ import division  # Required for floating point division.
from heapq import heappush, heappop  # Required for heap operations of schedule.
from NumberGenerator import exponentialValue  # Required to generate exponentially distributed random numbers


class Controller:
    def __init__(self, arrivalRate, averageServiceTime, simulationTime):
        self.arrivalRate = arrivalRate
        self.serviceRate = 1 / averageServiceTime
        self.simulationTime = simulationTime
        self.time = 0
        self.queue = []  # A queue of events waiting to be served
        self.beingServed = None  # The request being served. None if no request is being served.
        self.monitor = Monitor()  # Collects information about the state of the queue.
        # Schedule is a heap with times as keys and events as values.
        # The events will be representing by the following strings:
        # "Birth", "Death", and "Monitor"
        self.schedule = []

    def runSimulation(self, monitorStartingTime):
        self.monitorStartingTime = monitorStartingTime
        # Add first Birth event to schedule
        heappush(self.schedule, (exponentialValue(self.arrivalRate), "Birth"))
        # Add first Monitor event to schedule.
        heappush(self.schedule, (monitorStartingTime, "Monitor"))

        while self.time < self.simulationTime:
            # Get the next event from the schedule
            pair = heappop(self.schedule)
            self.time = pair[0]
            event = pair[1]
            self.executeEvent(event)

    def executeEvent(self, event):
        if event == "Birth":
            # Create new request and enqueue
            newRequest = Request(self.time)
            self.queue.append(newRequest)
            # Schedule next birth
            timeOfNextBirth = self.time + exponentialValue(self.arrivalRate)
            heappush(self.schedule, (timeOfNextBirth, "Birth"))

            # If queue only has one request and no requests are being served, then
            # dequeue the request, start serving request, and schedule death
            if len(self.queue) == 1 and self.beingServed == None:
                request = self.queue.pop(0)
                request.setServiceTime(self.time)
                self.beingServed = request
                # Schedule a death
                deathTime = self.time + exponentialValue(self.serviceRate)
                heappush(self.schedule, (deathTime, "Death"))
        elif event == "Death":
            recentlyDied = self.beingServed
            recentlyDied.setDeathTime(self.time)
            if self.time > self.monitorStartingTime:
                self.monitor.recordDeadRequest(recentlyDied)
            self.beingServed = None
            # Now there are no requests being served. If queue is empty, do nothing. Otherwise serve next request.
            if len(self.queue) != 0:
                request = self.queue.pop(0)
                request.setServiceTime(self.time)
                self.beingServed = request
                # Schedule a death
                deathTime = self.time + exponentialValue(self.serviceRate)
                heappush(self.schedule, (deathTime, "Death"))
        else:
            # This must be a monitor event
            requestsWaiting = len(self.queue)
            requestsInSystem = requestsWaiting
            if self.beingServed != None:
                requestsInSystem += 1
            self.monitor.recordSnapshot(requestsWaiting, requestsInSystem)
            # Schedule next monitor event.
            nextMonitorTime = self.time + exponentialValue(self.arrivalRate / 2)
            heappush(self.schedule, (nextMonitorTime, "Monitor"))


class Request:
    def __init__(self, birthTime):
        self.birthTime = birthTime

    def setServiceTime(self, serviceTime):
        self.serviceTime = serviceTime

    def setDeathTime(self, deathTime):
        self.deathTime = deathTime

    def getWaitingTime(self):
        return self.serviceTime - self.birthTime

    def getQueuingTime(self):
        return self.deathTime - self.birthTime


class Monitor:
    def __init__(self):
        self.numSnapshots = 0
        self.numRequests = 0
        self.requestsWaiting = []
        self.requestsInSystem = []
        self.waitingTimes = []
        self.queuingTimes = []

    def recordSnapshot(self, requestsWaiting, requestsInSystem):
        self.numSnapshots += 1
        self.requestsWaiting.append(requestsWaiting)
        self.requestsInSystem.append(requestsInSystem)

    def recordDeadRequest(self, request):
        self.numRequests += 1
        self.waitingTimes.append(request.getWaitingTime())
        self.queuingTimes.append(request.getQueuingTime())

    def printReport(self):

        print("Average Requests Waiting: " + str(sum(self.requestsWaiting) / self.numSnapshots))
        print("Average Requests In System: " + str(sum(self.requestsInSystem) / self.numSnapshots))
        print("Average Waiting Time: " + str(sum(self.waitingTimes) / self.numRequests))
        print("Average Queuing Time: " + str(sum(self.queuingTimes) / self.numRequests))


print("Lambda = 50 and Ts = 0.015")
# Get controller ready for a simulation with the given Lambda, Ts, and simulation time of 400.
myController = Controller(50, 0.015, 400)
# Begin the simulation and start monitoring system at time 100.
myController.runSimulation(100)
# Print the results of the simulation
myController.monitor.printReport()
