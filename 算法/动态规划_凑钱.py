__doc__ = "动态规划  递归的暴力解法 -> 带备忘录的递归解法 -> 非递归的动态规划解法。"

coins = [1, 2, 5]  # 硬币种类
amount = 13  # 目标金额


def coinChange(coins: list, amount: int):
    """自顶而下，递归+无备忘录，n叉树的遍历"""

    def dp(n):
        if n == 0:
            return 0
        if n < 0:
            return -1
        res = float('INF')  # 正无穷
        for coin in coins:
            subproblem = dp(n - coin)
            # ⼦问题⽆解，跳过
            if subproblem == -1:
                continue
            res = min(res, 1 + subproblem)
        return res if res != float('INF') else -1

    return dp(amount)


print(coinChange(coins, amount))


def coinChangeMemo(coins: list, amount: int):
    """自顶而下，递归+备忘录"""
    memo = {0: 0}  # 备忘录

    def dp(n):
        if n < 0:
            return -1
        if n in memo:  # 查询备忘录，避免重复计算
            return memo[n]
        res = float('INF')  # 正无穷
        for coin in coins:
            subproblem = dp(n - coin)
            # ⼦问题⽆解，跳过
            if subproblem == -1:
                continue
            res = min(res, 1 + subproblem)
            memo[n] = res if res != float('INF') else -1  # 将结果记入备忘录
        return memo[n]

    return dp(amount), memo


print(coinChangeMemo(coins, amount))


def coinChangeDp1(coins: list, amount: int):
    """自底向上，迭代+dp table"""
    mx = amount + 1
    dp = {0: 0, amount: mx}  # dp table dp[i]=x表示当金额为i时至少需要x枚硬币
    i = 0
    while i < mx:
        for x in coins:
            t = i - x
            if t < 0:
                continue  # 子问题无解
            dp[i] = min(dp.get(i, amount), 1 + dp.get(t, amount))
        i += 1
    print(dp)
    return dp[amount] if dp[amount] != amount + 1 else -1


print(coinChangeDp1(coins, amount))

from collections import defaultdict


def coinChangeDp2(coins: list, amount: int):
    """自底向上，迭代+dp table"""
    # 从字典向外拿数据. 字典是空的. key:callable() 这里的[]和get()不是一回事
    dp = defaultdict(lambda: amount)  # dp table dp[i]=x表示当金额为i时至少需要x枚硬币
    dp[0] = 0
    mx = amount + 1
    dp[amount] = mx  # 全用1元硬币最多需要amount个,amount+1相当于前面例子的float('INF')

    i = 0
    while i < mx:  # 从0构建dp table，遍历后的dp[i]就是金额凑到i时所有需要的最小枚树
        for x in coins:  # 每枚硬币都尝试一遍
            t = i - x
            if t < 0:
                continue
            # dp[i]的最小值，要么是全是1凑成的，要么是已经存在的d[t]再加一枚面值为x的硬币凑成。
            # 可以看到凑钱的动态转移方程不是像斐波那契数列中dp[i]只和dp[i-1],dp[i-2]有关系。
            # 而是变成了dp[i]和dp[i-:coins[0]:i-coins[-1]]之间的某个值有关。
            # 就像爬楼梯中一样，每次最多跨3个台阶。
            # 这也是为什么斐波那契数列中只需要一个while循环，而凑钱中需要在while中加一个尝试在coins再找个值试试的原因。
            dp[i] = min(dp[i], 1 + dp[t])
        i += 1
    print(dp)
    return dp[amount] if dp[amount] != amount + 1 else -1


print(coinChangeDp2(coins, amount))
