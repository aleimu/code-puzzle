__doc__ = "参数数量 参数分配到寄存器上还是栈上？是不是边界值6？"


a, b, c, d, e, f, g, h, i, j, k = 1, 2, 3, 4, '5', '6', '7', '8', '9', '10', '11'

arg_dict = {'a': a, 'b': b, 'c': c, 'd': d, 'e': e, 'f': f}
print(arg_dict.keys())
print(arg_dict.values())


def test(a, b, c, d):
    return a, b, c, d


def test0(a, b, c, d, e):
    return a, b, c, d, e


def test1(a, b, c, d, e, f):
    return a, b, c, d, e, f


def test11(a, b, c, d, e, f, h):
    return a, b, c, d, e, f, h


def test111(a, b, c, d, e, f, g, h):
    return a, b, c, d, e, f, g, h


def test1111(a, b, c, d, e, f, g, h, i):
    return a, b, c, d, e, f, g, h, i


def test11111(a, b, c, d, e, f, g, h, i, j):
    return a, b, c, d, e, f, g, h, i, j


def test2(arg_dict):
    return arg_dict


if __name__ == '__main__':
    import timeit
    from timeit import Timer

    t = Timer("test(%s,%s,%s,%s)" % (a, b, c, d), "from __main__ import test")
    t0 = Timer("test0(%s,%s,%s,%s,%s)" % (a, b, c, d, e), "from __main__ import test0")
    t1 = Timer("test1(%s,%s,%s,%s,%s,%s)" % (a, b, c, d, e, f), "from __main__ import test1")
    t11 = Timer("test11(%s,%s,%s,%s,%s,%s,%s)" % (a, b, c, d, e, f, h), "from __main__ import test11")
    t111 = Timer("test111(%s,%s,%s,%s,%s,%s,%s,%s)" % (a, b, c, d, e, f, h, i), "from __main__ import test111")
    t1111 = Timer("test1111(%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (a, b, c, d, e, f, h, i, j), "from __main__ import test1111")
    t11111 = Timer("test11111(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (a, b, c, d, e, f, g, h, i, j),
                   "from __main__ import test11111")
    t2 = Timer("test2(%s)" % arg_dict, "from __main__ import test2")

    print(t.timeit(100000))
    print(t0.timeit(100000))
    print(t1.timeit(100000))
    print(t11.timeit(100000))
    print(t111.timeit(100000))
    print(t1111.timeit(100000))
    print(t11111.timeit(100000))
    print(t2.timeit(100000))
