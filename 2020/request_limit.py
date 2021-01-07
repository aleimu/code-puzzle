# -*- coding:utf-8 -*-

import json
from flask import Flask, jsonify, request
from flask_limiter import Limiter, HEADERS  # https://github.com/alisaifee/flask-limiter
from flask_limiter.util import get_remote_address

# -*- coding:utf-8 -*-
__author__ = "aleimu"
__date__ = "2018.9.28"

# 限制接口短时间调用次数

import redis
import time
from flask import Flask, jsonify, request
from functools import wraps

REDIS_DB = 0
REDIS_HOST = '172.16.4.120'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
IP_LIMIT = 10
TIME_LIMIT = 60

app = Flask(__name__)
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, socket_timeout=3000)


def repeat_intercept(ex=5, ip_path=True):  # 第一层包装自定义闭包参数
    """拦截重复请求 ex默认5秒"""

    def decorator(func):  # 第二层包装主函数
        @wraps(func)
        def function(*args, **kwargs):  # 第三层包装主函数的参数
            req_str = "intercept:"
            if ip_path:
                req_str += request.remote_addr + request.path  # 只对ip和url做限制
            else:
                req_dict = request.values.to_dict()
                req_str += json.dumps(sorted([(x, y) for x, y in req_dict.items()]))  # 对请求的参数也做校验
            if r.exists(req_str):
                return jsonify({"code": 1404, "errmsg": "请求频率过高", "data": None})
            else:
                r.set(req_str, 0, ex)
                return func(*args, **kwargs)

        return function

    return decorator


@app.route("/call")
@repeat_intercept(ex=1, ip_path=True)
def home():
    return jsonify({'code': 200, 'status': "", 'message': {}})


@app.route("/")
@repeat_intercept(ex=5, ip_path=False)
def index():
    return jsonify({'code': 200, 'status': "", 'message': {}})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
