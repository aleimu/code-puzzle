__doc__ = '斐波那契数列 递归+备忘录 自顶向下 空间换时间'

"""
动态规划问题一般都是求最值,既然是求最值那核心问题就是穷举,并且聪明的避免重复计算(重叠子问题),
一般优化的方案是使用[备忘录]或者 [dp table].

备忘录可以是数组,字典,也可以是几个数字
dp table 和备忘录差不多,但当遍历玩全部值后,dp table会记录所有子问题的解.
一般不用刻意区分.

状态转移方程包括了状态和转移
状态就是原问题和子问题中的变量,
转移可以理解为递归关系

最优子结构 + 状态转移方程 + 备忘录/dp table = 动态规划


"""


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
