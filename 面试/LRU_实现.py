# coding: utf-8
__doc__ = """
LRU（The Least Recently Used，最近最久未使用算法）是一种常见的缓存算法，在很多分布式缓存系统（如Redis, Memcached）中都有广泛使用。
双向链表（LinkedList）+哈希表（HashMap）实现（链表用来表示位置，哈希表用来存储和查找），
在Java里有对应的数据结构LinkedHashMap。python中的collections.OrderedDict,functools.lru_cache已经实现了可以参考.

https://leetcode-cn.com/problems/lru-cache/solution/
"""

import collections


class LRUCache(collections.OrderedDict):
    def __init__(self, size=5):
        self.size = size,
        self.cache = collections.OrderedDict()

    def get(self, key):
        if key in self.cache:
            val = self.cache.pop(key)
            self.cache[key] = val
        else:
            val = None

        return val

    def set(self, key, val):
        if key in self.cache:
            val = self.cache.pop(key)
            self.cache[key] = val
        else:
            if len(self.cache) == self.size:
                self.cache.popitem(last=False)
                self.cache[key] = val
            else:
                self.cache[key] = val


if __name__ == '__main__':
    """ test """
    cache = LRUCache(6)

    for i in range(10):
        cache.set(i, i)

    for i in range(10):
        import random

        i = random.randint(1, 20)
        print('cache', list(cache.cache.keys()))
        if cache.get(i):
            print('hit, %s\n' % i)
        else:
            print('not hit, %s\n' % i)
