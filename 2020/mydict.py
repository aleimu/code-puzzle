# python3.6
from collections import namedtuple


class SimpleArray(object):
    # 简单的数组类实现

    def __init__(self, mix):
        self.container = [None for i in range(mix)]

    def __len__(self):
        return len(self.container)

    def __setitem__(self, key, value):
        return self.container.__setitem__(key, value)

    def __getitem__(self, item):
        return self.container.__getitem__(item)

    def __delitem__(self, key):
        return self.container.__setitem__(key, None)

    def __str__(self):
        return str(self.container)


class SimpleDict(object):
    # 简单的字典类实现

    Init_length = 8  # 初始化的大小
    Load_factor = 2 / 3  # 扩容因子

    def __init__(self):
        self._array_len = SimpleDict.Init_length
        self._array = SimpleArray(self._array_len)
        self._used = 0
        self.dictObj = namedtuple("dictObj", "key value")  # 这里其实可以用数组也可以的，namedtuple是为了让代码更可读

    def __getitem__(self, item):
        key = self._hash(item)
        dictObj = self._array[key]
        if dictObj is not None and dictObj.key == item:
            return dictObj.value
        else:
            for new_key in self._second_hash(key):
                if self._array[new_key] is not None and item == self._array[new_key].key:
                    return self._array[new_key].value

    def __setitem__(self, key, value):
        # 计算是否需要扩容
        if (self._used / self._array_len) > SimpleDict.Load_factor:
            self._new_array()

        # 根据键的hash值来计算得出位置索引
        hash_key = self._hash(key)
        new_key = self._second_hash(hash_key)

        while True:
            if self._array[hash_key] is None or key == self._array[hash_key].key:
                break

            # 发生哈希碰撞根据二次探查函数得出下一个索引的位置
            hash_key = next(new_key)

            if abs(hash_key) >= self._array_len:
                self._new_array()
                hash_key = self._hash(key)

        # 找到空位将键值对象放入
        self._array[hash_key] = self.dictObj(key, value)
        self._used += 1

    def __delitem__(self, key):
        hash_key = self._hash(key)
        if key != self._array[hash_key].key:
            for new_key in self._second_hash(hash_key):
                if key == self._array[new_key].key:
                    hash_key = new_key

        self._array[hash_key] = None
        self._used -= 1

    def _hash(self, key):
        # 计算哈希值
        return hash(key) & (self._array_len - 1)

    def _second_hash(self, hash_key):
        # 简单的二次探查函数实现
        count = 1
        for i in range(self._array_len):
            new_key = hash_key + count ** 2
            if abs(new_key) < self._array_len:
                yield new_key

            new_key = hash_key - count ** 2
            if abs(new_key) < self._array_len:
                yield new_key

            count += 1

    def _new_array(self):
        # 扩容
        old_array = self._array
        self._array_len = self._array_len * 2  # 扩容2倍大小
        self._array = SimpleArray(self._array_len)
        for i in range(len(old_array)):
            dictObj = old_array[i]
            if dictObj is not None:
                self[dictObj.key] = dictObj.value

    def __str__(self):
        result = ", ".join("%s:%s" % (obj.key, obj.value)
                           for obj in self._array
                           if obj is not None)
        return "{" + result + "}"


if __name__ == '__main__':
    d = SimpleDict()
    for i in range(20):
        d[str(i)] = i
    print(d)
    print(d["10"])
    del d["11"]
    print(d)