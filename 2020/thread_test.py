#!/usr/bin/python3

import threading
import time
import random

exitFlag = 0

# 进程变量+
ProcessVar = {"a": 1, "b": 2, "c": 3}


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        for x in range(10):
            print("开始线程：" + self.name, ProcessVar)
            ProcessVar[self.name] = (random.randint(1, 10), x)
            time.sleep(1)
            print("退出线程：" + self.name, ProcessVar)


# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("退出主线程")
