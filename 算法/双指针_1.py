__doc__ = "将素组中的非0元素放到数组前边，并保持非0元素之家的顺序"


def leetcode1(ls: list):
    """双指针法"""
    n = 0
    for k, v in enumerate(ls):
        # print(k,v)
        if v != 0:
            ls[n] = v
            ls[k] = 0
            n = n + 1
            # print(ls, n)
    print(ls)
    return ls


leetcode1([0, 1, 2, 3, 0, 5, 0, 5, 0, 4, 3, 2, 0, 0, 0])
