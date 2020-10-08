__doc__ = '斐波那契数列 递归+备忘录 自顶向下 空间换时间'


def fib(n: int):
    """自顶而下，递归"""
    if n == 1 or n == 2:
        return 1
    return fib(n - 1) + fib(n - 2)


print(fib(10))  # 纯递归，无备忘录

memo = {1: 1, 2: 1}  # 初始化备忘录


def fib_memo(n: int):
    """自顶而下，递归+备忘录"""
    if n not in memo:
        memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]


print(fib_memo(10))  # 递归+备忘录

"""
带「备忘录」的递归算法，把一棵存在巨量冗余的递归树通过「剪枝」，改造成了一幅不存在冗余的递归图，极大减少了子问题（即递归图中节点）的个数。
"""


def fib_iter(n: int):
    """迭代解法，自低向上"""
    dp = {}
    dp[1] = dp[2] = 1
    i = 3
    while i <= n:
        dp[i] = dp[i - 1] + dp[i - 2]
        i += 1
    return dp[n], dp


print(fib_iter(10))


def fib_iter(n: int):
    """迭代解法，自低向上，迭代时只需要最近两个值，可以进一步优化，减少空间"""
    if n < 3:
        return 1
    a, b, i = 1, 1, 3
    while i <= n:
        a, b = b, a + b
        i += 1
    return b, a, b


print(fib_iter(10))
