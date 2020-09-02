#!/usr/bin/python3
# coding:utf-8

import socket
import time
import os

path = 'bigfile'


# 传统的拷贝文件
def copyclient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 10000)
    sock.connect(server_address)

    start = time.time()
    try:
        with open(path, 'rb') as f:
            message = f.read()
            sock.sendall(message)
    finally:
        sock.close()

    end = time.time()
    print('Total time: ', end - start)


# 零拷贝实现 - Python 3.3
def zerocopyclient():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 10000)
    sock.connect(server_address)

    start = time.time()
    try:
        with open(path, 'rb') as f:
            # message = f.read()
            # sock.sendall(message)
            ret = 0
            offset = 0

            while True:
                ret = os.sendfile(sock.fileno(), f.fileno(), offset, 65536)
                offset += ret
                if ret == 0:
                    break
    finally:
        sock.close()

    end = time.time()
    print('Total time: ', end - start)


# 零拷贝实现 - python 3.5
def zerocopyclient2():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 10000)
    sock.connect(server_address)

    start = time.time()
    try:
        with open(path, 'rb') as f:
            while True:
                sock.sendfile(f, 0)
                break
    finally:
        sock.close()
    end = time.time()
    print('Total time: ', end - start)


copyclient()
zerocopyclient()
zerocopyclient2()
