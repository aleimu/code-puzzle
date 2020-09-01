import os
import time
from flask import Flask, request, Response
from threading import get_ident

app = Flask(__name__)


@app.route('/1', methods=['GET', "POST", "PUT", "DELETE"])
def test1():
    thread_id = get_ident()  # 获取处理此请求的线程id
    pid = os.getpid()  # 获取当前进程id
    ppid = os.getppid()  # 获取父进程id
    req = f'thread1:{thread_id},pid:{pid},ppid:{ppid}'
    print(req)
    time.sleep(5)
    return Response(req)


@app.route('/2', methods=['GET', "POST", "PUT", "DELETE"])
def test2():
    thread_id = get_ident()  # 获取处理此请求的线程id
    pid = os.getpid()  # 获取当前进程id
    ppid = os.getppid()  # 获取父进程id
    req = f'thread2:{thread_id},pid:{pid},ppid:{ppid}'
    print(req)
    time.sleep(5)
    return Response(req)


if __name__ == "__main__":
    app.run(threaded=True, )
    app.run(processes=1, )

"""window上查看进程id
# tasklist |findstr.exe py
pycharm64.exe                11520 Console                    1  1,130,168 K
python.exe                    5536 Console                    1     28,984 K

# 尝试多次请求接口，可以看到每次thread_id都不一样，py进程id不变以及其父进程id也不变。

# curl 127.0.0.1:5000/1
thread1:4604,pid:9164,ppid:11520

# curl 127.0.0.1:5000/2
thread2:3008,pid:9164,ppid:11520
"""
