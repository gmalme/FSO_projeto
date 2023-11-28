from queue import Queue
from process.process import Process
from utils.output import Output
from utils.messages import *


class UserQueue:
    def __init__(self) -> None:
        self.out = Output()
        self.q1 = Queue()  # RR 1-20
        self.q2 = Queue()  # RR 21-49
        self.q3 = Queue()  # RR >= 50
        self.Q1_MAX_PRIORITY = 20
        self.Q2_MAX_PRIORITY = 21
        self.Q3_MAX_PRIORITY = 50
        self.Q1_QUANTUM = 5
        self.Q2_QUANTUM = 10
        self.Q3_QUANTUM = 15
        self.AGING_WAITING_TIME = 5

    def get_queue_quantum(self, queue):
        if queue == self.q1:
            return self.Q1_QUANTUM
        if queue == self.q2:
            return self.Q2_QUANTUM
        return self.Q3_QUANTUM

    def put(self, process: Process):
        if process.priority <= self.Q1_MAX_PRIORITY:
            self.q1.put(process)
        elif self.Q1_MAX_PRIORITY < process.priority < self.Q3_MAX_PRIORITY:
            self.q2.put(process)
        else:
            self.q3.put(process)

    def empty(self):
        return all(queue.empty() for queue in [self.q1, self.q2, self.q3])

    def get(self):
        for queue in [self.q1, self.q2, self.q3]:
            if not queue.empty():
                return queue.get(), queue

    def qsize(self):
        return sum(queue.qsize() for queue in [self.q1, self.q2, self.q3])

    def down(self, process, last_queue, interrupt):
        if not process:
            return

        if interrupt:
            last_queue.put(process)
            return

        priority_increase = 6 if last_queue == self.q2 else 8
        process.priority = min(self.Q3_MAX_PRIORITY - 1, process.priority + priority_increase)
        self.q3.put(process)
        self.out.debug(DOWN_PROCESS, pid=process.pid, queue=3)

    def aging(self):
        for queue in [self.q1, self.q2, self.q3]:
            for proc in queue.queue:
                proc.waiting_time += 1
                if proc.waiting_time % self.AGING_WAITING_TIME == 0:
                    proc.priority = max(1, proc.priority - 1)

    def up(self):
        q2 = self.q2.queue.copy()
        q3 = self.q3.queue.copy()

        for process in self.q2.queue:
            if process.priority <= self.Q1_MAX_PRIORITY:
                self.q1.put(process)
                q2.remove(process)
                self.out.debug(UP_PROCESS, pid=process.pid, queue=1)

        for process in self.q3.queue:
            if self.Q1_MAX_PRIORITY < process.priority < self.Q3_MAX_PRIORITY:
                self.q2.put(process)
                q3.remove(process)
                self.out.debug(UP_PROCESS, pid=process.pid, queue=2)

        self.q2.queue = q2.copy()
        self.q3.queue = q3.copy()
