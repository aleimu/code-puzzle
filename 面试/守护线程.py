# -*- coding: utf-8 -*-
import threading
import time


def send_message(mes):
    print("before send message")
    time.sleep(2)
    print("after send message")


def get_message(mes):
    print("before get message")
    time.sleep(2)
    print("after get message")


# if __name__ == "__main__":
#     thread1 = threading.Thread(target=send_message, args=("",))
#     thread2 = threading.Thread(target=get_message, args=("",))
#     thread1.start()
#     thread2.start()
#     print("主线程执行完毕")
if __name__ == "__main__":
    thread1 = threading.Thread(target=send_message, args=("",))
    thread2 = threading.Thread(target=get_message, args=("",))
    thread1.setDaemon(True)  # 设置守护进程
    thread2.setDaemon(True)
    thread1.start()
    thread2.start()
    print("主线程执行完毕")
    # time.sleep(3)

"""
之前我们接触的线程都是在前台运行的，它们也叫前台线程，而有的线程在后台运行，它运行的目的是为了给其它线程提供服务，这样的线程称为后台线程，也叫做守护线程。
例如，Python解释器中的垃圾回收线程就是一种后台线程。
所有线程都有一个daemon属性。它用来把线程设置为后台线程，因为它默认为False，所以我们此前创建的线程都是前台线程，当把它设置为True时，该线程就成了后台线程。
后台线程依托于前台线程，当前台线程已经全部死亡的时候，后台线程也会随之死亡。
后台线程有一个特征，如果所有的前台线程都死亡了，那么后台线程会自动死亡。
可见，创建后台线程有两种方式：
1.主动将线程的 daemon 属性设置为 True。
2.后台线程启动的线程默认是后台线程。

"""
