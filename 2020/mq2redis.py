# -*- coding:utf-8 -*-
__doc__ = '特以此文件起服务做中间转发操作,此文件为单服务多进程服务模式,脚本独立启动与启动一组mq_toredis.py的功能是一致的,但此处为类式实现'
__doc2__ = 'rocketmq对python的支持很不友好,rocketmq.client的核心方法都是在.so文件,这里记录下当需要启动多实例的client时改怎么处理'

import uuid
import json
import redis
import argparse
import traceback
import datetime
from rocketmq.client import PushConsumer
from multiprocessing import Process

try:
    from rocketmq.client import _CConsumeStatus as ConsumeStatus
except:
    from rocketmq.client import ConsumeStatus

from config import *

# mq的tag转发到redis队列的对应关系
ParserDict = {
    TAG_LIN: [TOPIC, NAME_SERVER, CONSUMER_GROUP_LIN, TAG_LIN, RDS_LIN],  # 线路
    TAG_SEC: [TOPIC, NAME_SERVER, CONSUMER_GROUP_SEC, TAG_SEC, RDS_SEC],  # 线路路段
    TAG_FRE: [TOPIC, NAME_SERVER, CONSUMER_GROUP_FRE, TAG_FRE, RDS_FRE],  # 频次
    TAG_DET: [TOPIC, NAME_SERVER, CONSUMER_GROUP_DET, TAG_DET, RDS_DET],  # 频次明细
    TAG_MIL: [TOPIC, NAME_SERVER, CONSUMER_GROUP_MIL, TAG_MIL, RDS_MIL]  # 里程

}

parser = argparse.ArgumentParser(description='accept rocketmq data and forward to redis')
parser.add_argument('-name', '--name', type=str, required=False,
                    help='run task with the input name:{}'.format(ParserDict.keys()))
args = parser.parse_args()
rds = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_CAMEL)


class Mq2Redis:
    def __init__(self, topic, name_server, consumer, tag, queue, key='key'):
        """
        topic:mq的topic
        name_server:mq的服务ip集合
        consumer:mq的消费者名
        tag:mq的topic下分的tag
        queue:redis队列名
        key:消息body中唯一标志值
        """
        self.tag = tag
        self.key = key
        self.queue = queue
        p = Process(target=self.start, args=(topic, name_server, consumer))
        p.start()

    def start(self, topic, name_server, consumer):
        Consumer = PushConsumer(consumer)
        try:
            Consumer.set_namesrv_addr(name_server)
        except:
            traceback.print_exc()
            Consumer.set_name_server_address(name_server)
        Consumer.subscribe(topic, self.run)
        Consumer.start()
        print("run {} task success and into the loop, wait for the message!".format(name_server))
        while True:  # 这里是必须的,而且每个实例都必须有单独的while阻塞,不可以共用. TODO
            pass

    def run(self, msg):
        """mq数据转存入redis中"""
        print("Mq2Redis.run <---data:", datetime.datetime.now(), msg.id, msg.topic, msg.keys, msg.tags, msg.body)
        if msg.tags == self.tag:
            try:
                jg_data = json.loads(msg.body, encoding='utf-8')
                key = jg_data.get(self.key, None)
                if not key:
                    key = uuid.uuid1()
                rds.set(key, msg.body)
                rds.lpush(self.queue, key)
                print("mq data push redis success!")
            except:
                traceback.print_exc()
                return ConsumeStatus.RECONSUME_LATER
            return ConsumeStatus.CONSUME_SUCCESS


def choice_start(name):
    if name:
        if name not in ParserDict.keys():
            print("The choice {} not in:{}, Program exit!".format(name, ParserDict.keys()))
        else:
            # 启动单进程实例
            args = ParserDict.get(name)
            Mq2Redis(args[0], args[1], args[2], args[3], args[4])
            print("run {} task success!".format(name))
            while True:
                pass
    else:
        # 启动多进程实例
        Mq2Redis(TOPIC, NAME_SERVER, CONSUMER_GROUP_LIN, TAG_LIN, RDS_LIN)
        Mq2Redis(TOPIC, NAME_SERVER, CONSUMER_GROUP_SEC, TAG_SEC, RDS_SEC)
        Mq2Redis(TOPIC, NAME_SERVER, CONSUMER_GROUP_FRE, TAG_FRE, RDS_FRE)
        Mq2Redis(TOPIC, NAME_SERVER, CONSUMER_GROUP_DET, TAG_DET, RDS_DET)
        Mq2Redis(TOPIC, NAME_SERVER, CONSUMER_GROUP_MIL, TAG_MIL, RDS_MIL)
        print("run all task success!")
        while True:
            pass


if __name__ == '__main__':
    choice_start(args.name)

"""
关于此脚本的管理是使用了supervisord
要是按多进程方式启动的话,需要在/etc/supervisord.d/line.conf配置文件中如下配置,这样才能同步管理子进程.最后记得supervisorctl update下.
stopasgroup = true
killasgroup = true
"""





