import threading
import time


def run():
    a = 123
    time.sleep(1)
    print('当前线程的名字是： ', threading.current_thread().name, b)
    time.sleep(1)


def run2():
    b = 321
    time.sleep(1)
    print('当前线程的名字是： ', threading.current_thread().name, a)
    time.sleep(1)


print('这是主线程：', threading.current_thread().name)
thread_list = []
for i in range(5):
    t = threading.Thread(target=run)
    thread_list.append(t)

for t in thread_list:
    t.start()

print('主线程结束！', threading.current_thread().name)
