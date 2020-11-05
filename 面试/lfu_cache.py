__doc__ = "模仿functools.lru_cache 实现的lfu_cache"


import functools
from heapq import nsmallest
from operator import itemgetter


class Counter(dict):
    def __missing__(self, key):
        return 0


def lfu_cache(maxsize=100):
    def decorating_function(user_function):
        cache = {}  # mapping of args to results
        use_count = Counter()  # times each key has been accessed
        kwd_mark = object()  # separate positional and keyword args

        @functools.wraps(user_function)
        def wrapper(*args, **kwds):
            key = args
            if kwds:
                key += (kwd_mark,) + tuple(sorted(kwds.items()))
            use_count[key] += 1

            # get cache entry or compute if not found
            try:
                result = cache[key]
                wrapper.hits += 1
            except KeyError:
                result = user_function(*args, **kwds)
                cache[key] = result
                wrapper.misses += 1

                # purge least frequently used cache entry
                if len(cache) > maxsize:
                    for key, _ in nsmallest(maxsize // 10,
                                            iter(use_count.items()),
                                            key=itemgetter(1)):
                        del cache[key], use_count[key]

            return result

        def clear():
            cache.clear()
            use_count.clear()
            wrapper.hits = wrapper.misses = 0

        wrapper.hits = wrapper.misses = 0
        wrapper.clear = clear
        return wrapper

    return decorating_function


if __name__ == '__main__':

    @lfu_cache(maxsize=20)
    def f(x, y):
        return 3 * x + y


    domain = list(range(5))
    from random import choice

    for i in range(1000):
        r = f(choice(domain), choice(domain))

    print((f.hits, f.misses))
