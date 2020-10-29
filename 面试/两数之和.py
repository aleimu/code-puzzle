__doc__ = """
https://leetcode-cn.com/problems/two-sum
"""

nums = [2, 7, 11, 15]
target = 9


def twoSum(nums: list, target: int):
    """最慢"""
    for k, v in enumerate(nums):
        if target - v in nums:
            return k, nums.index(target - v)


print(twoSum(nums, target))


def twoSum(nums, target):
    """用字典加速"""
    hashmap = {}
    for ind, num in enumerate(nums):
        hashmap[num] = ind
    for i, num in enumerate(nums):
        j = hashmap.get(target - num)
        if j is not None and i != j:
            return [i, j]


print(twoSum(nums, target))


def twoSum(nums: list, target: int) -> list:
    """最优解,单次遍历"""
    cache = dict()  # cache用于记录值及其对应值的索引
    for idx, num in enumerate(nums):
        if num in cache:
            return [cache.get(num), idx]
        cache[target - num] = idx  # 把 差值 作为键/位置索引作为值赋给hashmap(注意位置别颠倒)


print(twoSum(nums, target))


class Solution:
    """N数之和"""

    def threeSum(self, nums: list) -> list:
        if not nums: return []

        # 先排序，关键！
        nums.sort()
        ans = set()
        N, target = 3, 0
        self._find_sum(nums, 0, N, target, [], ans)
        return list(ans)

    def _find_sum(self, nums, start, N, target, path, ans):
        # terminator
        if len(nums) < N or N < 2: return
        # process
        if N == 2:
            # 两数求和
            d = set()
            for j in range(start, len(nums)):
                if target - nums[j] in d:
                    ans.add(tuple(path + [target - nums[j], nums[j]]))
                else:
                    d.add(nums[j])
        else:
            for i in range(start, len(nums)):
                # 剪枝1: target比剩余数字能组成的最小值还要小 或 比能组成的最大值还要大，就可以停止循环了
                if target < nums[i] * N or target > nums[-1] * N: break
                # 剪枝2: 去重
                if i > start and nums[i] == nums[i - 1]: continue
                # drill down
                self._find_sum(nums, i + 1, N - 1, target - nums[i], path + [nums[i]], ans)
        return


# https://leetcode-cn.com/problems/3sum/solution/jian-ji-tong-yong-xie-fa-nshu-zhi-he-pythonxiang-x/

class Solution:
    def threeSum(self, nums: [int]) -> [[int]]:
        nums.sort()
        res, k = [], 0
        for k in range(len(nums) - 2):
            if nums[k] > 0: break  # 1. because of j > i > k.
            if k > 0 and nums[k] == nums[k - 1]: continue  # 2. skip the same `nums[k]`.
            i, j = k + 1, len(nums) - 1
            while i < j:  # 3. double pointer
                s = nums[k] + nums[i] + nums[j]
                if s < 0:
                    i += 1
                    while i < j and nums[i] == nums[i - 1]: i += 1
                elif s > 0:
                    j -= 1
                    while i < j and nums[j] == nums[j + 1]: j -= 1
                else:
                    res.append([nums[k], nums[i], nums[j]])
                    i += 1
                    j -= 1
                    while i < j and nums[i] == nums[i - 1]: i += 1
                    while i < j and nums[j] == nums[j + 1]: j -= 1
        return res

# https://leetcode-cn.com/problems/3sum/solution/3sumpai-xu-shuang-zhi-zhen-yi-dong-by-jyd/
