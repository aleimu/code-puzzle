# -*- coding:utf-8 -*-
__author__ = "leimu"
__date__ = "2019-09-23"
__doc__ = "待完善"

from sanic import Sanic, response
from sanic.response import text

app = Sanic()


@app.route("/")
async def index(request):
    return text('Hello World!')


test_json = {
    "code": 1000,
    "data": {
        "count": 374,
        "users": [
                     {
                         "active": 0,
                         "com_type": 0,
                         "create_time": "2019-08-06 09:40:43",
                         "delete_flag": 0,
                         "email": False,
                         "fk_dept_id": "1",
                         "fk_location_code": False,
                         "fullname": "呵呵呵",
                         "fullname2": "\u82cf\u82cf\u82cf",
                         "id": 2659,
                         "mobile": "15555555555",
                         "photo_url": False,
                         "reason": "",
                         "role_type": 0,
                         "source": 2,
                         "telephone": "15555555555",
                         "update_time": "2019-09-20 13:22:24",
                         "user_no": False,
                         "user_type": 2,
                         "username": "15555555555",
                         "zh_name": "呵呵呵"
                     }
                 ] * 100
    },
    "errmsg": False
}
########################################################################################################################

import redis

rc = redis.StrictRedis(host="120.27.110.143", port=6379, password="", db=1, socket_timeout=3000)


@app.route('/json')
async def handle_request(request):
    rc.set("val", "value")
    test_json["val"] = str(rc.get("val"), encoding="utf-8")
    return response.json(test_json)


""" 同步-单进程-单核
Concurrency Level:      100
Time taken for tests:   61.118 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      43666000 bytes
HTML transferred:       43573000 bytes
Requests per second:    16.36 [#/sec] (mean)
Time per request:       6111.800 [ms] (mean)
Time per request:       61.118 [ms] (mean, across all concurrent requests)
Transfer rate:          697.71 [Kbytes/sec] received
"""

########################################################################################################################
import aioredis


# 用协程的话,好像就无法使用redis连接的单例了
@app.route('/json1')
async def handle_request(request):
    val = await redis_test1()
    test_json["val"] = val
    return response.json(test_json)


async def redis_test1():
    conn = await aioredis.create_redis_pool('redis://120.27.110.143', encoding="utf-8")
    # for x in range(100):
    #     await conn.set('my-key' + str(x), x)  # 这步有点耗时啊
    await conn.set('my-key', 'value')
    val = await conn.get('my-key')
    conn.close()
    await conn.wait_closed()
    return val


"""异步-单进程-多核
Concurrency Level:      100
Time taken for tests:   24.595 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      436660000 bytes
HTML transferred:       435730000 bytes
Requests per second:    406.59 [#/sec] (mean)
Time per request:       245.950 [ms] (mean)
Time per request:       2.459 [ms] (mean, across all concurrent requests)
Transfer rate:          17337.91 [Kbytes/sec] received
"""
########################################################################################################################
import asyncio_redis  # 评估了下,可用性不高,卡顿,连接数太多等


@app.route('/json2')
async def handle_request(request):
    val = await redis_test2()
    test_json["val"] = val
    return response.json(test_json)


async def redis_test2():
    # Create Redis connection
    # conn = await asyncio_redis.Connection.create(host='120.27.110.143', port=6379)
    conn = await asyncio_redis.Pool.create(host='120.27.110.143', port=6379, poolsize=10)
    for x in range(100):
        await conn.set('my-key' + str(x), str(x))
    # Set a key
    await conn.set('my_key', 'my_value')
    val = await conn.get('my-key')
    # When finished, close the connection.
    conn.close()
    return val


"""异步-单进程-多核
Concurrency Level:      100
Time taken for tests:   2.632 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      43666000 bytes
HTML transferred:       43573000 bytes
Requests per second:    379.94 [#/sec] (mean)
Time per request:       263.200 [ms] (mean)
Time per request:       2.632 [ms] (mean, across all concurrent requests)
Transfer rate:          16201.59 [Kbytes/sec] received

ValueError: too many file descriptors in select()
当数量大的时候,会出现卡顿,奇怪....
Concurrency Level:      100
Time taken for tests:   70.617 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      436660000 bytes
HTML transferred:       435730000 bytes
Requests per second:    141.61 [#/sec] (mean)
Time per request:       706.170 [ms] (mean)
Time per request:       7.062 [ms] (mean, across all concurrent requests)
Transfer rate:          6038.57 [Kbytes/sec] received

"""


async def main():
    pool = await aioredis.create_pool('redis://localhost', minsize=5, maxsize=10)
    with await pool as conn:  # low-level redis connection
        await conn.execute('set', 'my-key', 'value')
        val = await conn.execute('get', 'my-key')
    print('raw value:', val)
    pool.close()
    await pool.wait_closed()  # closing all open connections


########################################################################################################################
import aiomysql


@app.route('/json3')
async def handle_request(request):
    val = await mysql_test1()
    test_json["val"] = val
    return response.json(test_json)


async def mysql_test1():
    pool = await aiomysql.create_pool(host='120.27.110.143', port=3306, user='toto', password='toto123',
                                      db='camel_test')
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * from users limit 1;")
            print(cur.description)
            r = await cur.fetchone()
            print("r===", r)
    pool.close()
    await pool.wait_closed()
    return r


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3331)

'''
import uvloop
import aiotask_context as context

    asyncio.set_event_loop(uvloop.new_event_loop())
    server = app.create_server(host="0.0.0.0", port=8000, return_asyncio_server=True)
    loop = asyncio.get_event_loop()
    loop.set_task_factory(context.task_factory)
    task = asyncio.ensure_future(server)
    try:
        loop.run_forever()
    except:
        loop.stop()
'''
