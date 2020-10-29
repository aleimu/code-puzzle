__doc__ = """
https://leetcode-cn.com/problems/super-egg-drop/solution/ji-ben-dong-tai-gui-hua-jie-fa-by-labuladong/

要理解这个题的真正意思需要好好读一读上文,总结一句话就是:
正向: 给你 K 鸡蛋，N 层楼，让你求最坏情况下最少的测试次数 m  res = min(res, max(dp(K, N - i), dp(K - 1, i - 1)) + 1)
逆向: 给你 K 个鸡蛋，测试 m 次，最坏情况下最多能测试 N 层楼 dp[k][m] = dp[k][m - 1] + dp[k - 1][m - 1] + 1

要是还是不能理解的话,建议看李永乐老师锁的<<双蛋问题>>https://www.bilibili.com/video/BV1KE41137PK有较好的逻辑递进推导.
"""


def superEggDrop1(K: int, N: int):
    """正向解题"""
    memo = dict()

    def dp(K, N) -> int:
        # base case
        if K == 1: return N
        if N == 0: return 0
        # 避免重复计算
        if (K, N) in memo:
            return memo[(K, N)]
        res = float('INF')
        # 穷举所有可能的选择
        for n in range(1, N + 1):
            res = min(res, max(dp(K, N - n), dp(K - 1, n - 1)) + 1)
        # 记入备忘录
        memo[(K, N)] = res  # K 鸡蛋，N 层楼,最坏情况下最少的测试次数为res
        return res

    print("最少需要次数:", dp(K, N))
    print("***dp2***", memo)


def superEggDrop2(K: int, N: int) -> int:
    """反向解题"""
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    for m in range(1, N + 1):
        for k in range(1, K + 1):
            dp[m][k] = dp[m - 1][k] + dp[m - 1][k - 1] + 1
            # print("------", dp)
        if dp[m][K] >= N:  # dp[m][K] == N，也就是给你 K 个鸡蛋，测试 m 次，最坏情况下最多能测试 N 层楼
            print("最少需要次数:", m)
            print("***dp2***", dp)
            return m


# TODO 对superEggDrop2的一点点变换

def superEggDrop22(K: int, N: int) -> int:
    """反向解题"""
    dp = [[0] * (K + 1) for _ in range(N + 1)]
    m = 0
    while dp[m][K] < N:
        m += 1
        for k in range(1, K + 1):
            dp[m][k] = dp[m - 1][k - 1] + 1 + dp[m - 1][k]
    print("最少需要次数:", m)
    print("***dp3***", dp)
    return m


# TODO superEggDrop2  与 superEggDrop3 只是dp定义不一致,但都能正确求得结果

def superEggDrop3(K: int, N: int) -> int:
    """反向解题"""
    dp = [[0] * (N + 1) for _ in range(K + 1)]
    for m in range(1, N + 1):
        for k in range(1, K + 1):
            dp[k][m] = dp[k][m - 1] + dp[k - 1][m - 1] + 1
            # dp[k][m - 1] 就是楼上的楼层数，因为鸡蛋个数 k 不变，也就是鸡蛋没碎，扔鸡蛋次数 m 减一
            # dp[k - 1][m - 1] 就是楼下的楼层数，因为鸡蛋个数 k 减一，也就是鸡蛋碎了，同时扔鸡蛋次数 m 减一
            # m 是一个允许的次数上界，而不是扔了几次。
            # print("------", dp)
        if dp[K][m] >= N:  # dp[K][m] == N，也就是给你 K 个鸡蛋，测试 m 次，最坏情况下最多能测试 N 层楼
            print("最少需要次数:", m)
            print("***dp3***", dp)
            return m


# TODO 一维数组就能搞定,花半秒钟就看透事物本质的人,和花一辈子都看不清事物本质的人,注定是截然不同的命运

def superEggDrop4(K: int, N: int) -> int:
    """高手"""
    dp = [0] * (K + 1)
    drop = 0  # 操作次数
    while dp[K] < N:
        i = K
        print("***dp4***", dp)
        while i > 0:
            dp[i] = dp[i] + dp[i - 1] + 1  # 从后往前计算
            i = i - 1
        drop = drop + 1
    print("最少需要次数:", drop)
    print("***dp4***", dp)
    return drop


""" superEggDrop4
 /**
 * 鸡蛋掉落，鹰蛋（Leetcode 887）：（经典dp）
 * 有 K 个鸡蛋，有 N 层楼，用最少的操作次数 F 检查出鸡蛋的质量。
 *
 * 思路：
 * 本题应该逆向思维，若你有 K 个鸡蛋，你最多操作 F 次，求 N 最大值。
 *
 * dp[k][f] = dp[k][f-1] + dp[k-1][f-1] + 1;
 * 解释：
 * 0.dp[k][f]：如果你还剩 k 个蛋，且只能操作 f 次了，所能确定的楼层。
 * 1.dp[k][f-1]：蛋没碎，因此该部分决定了所操作楼层的上面所能容纳的楼层最大值
 * 2.dp[k-1][f-1]：蛋碎了，因此该部分决定了所操作楼层的下面所能容纳的楼层最大值
 * 又因为第 f 次操作结果只和第 f-1 次操作结果相关，因此可以只用一维数组。
 *
 * 时复：O(K*根号(N))
 */

作者：wat-2
链接：https://leetcode-cn.com/problems/super-egg-drop/solution/zhi-xing-yong-shi-0-ms-zai-suo-you-java-ti-jia-121/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

"""

superEggDrop1(K=2, N=10)
superEggDrop2(K=2, N=10)
superEggDrop3(K=2, N=10)
superEggDrop4(K=2, N=10)

"""几种解法的dp表
最少需要次数: 4
***dp2*** {(2, 1): 1, (2, 2): 2, (2, 3): 2, (2, 4): 3, (2, 5): 3, (2, 6): 3, (2, 7): 4, (2, 8): 4, (2, 9): 4, (2, 10): 4}
最少需要次数: 4
***dp2*** [[0, 0, 0], [0, 1, 1], [0, 2, 3], [0, 3, 6], [0, 4, 10], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
最少需要次数: 4
***dp3*** [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 0, 0, 0, 0, 0, 0], [0, 1, 3, 6, 10, 0, 0, 0, 0, 0, 0]]
最少需要次数: 4
***dp4*** [0, 4, 10]
"""
