__doc__ = """
你有一个带有四个圆形拨轮的转盘锁。每个拨轮都有10个数字： '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' 。每个拨轮可以自由旋转：例如把 '9' 变为  '0'，'0' 变为 '9' 。每次旋转都只能旋转一个拨轮的一位数字。
锁的初始数字为 '0000' ，一个代表四个拨轮的数字的字符串。
列表 deadends 包含了一组死亡数字，一旦拨轮的数字和列表里的任何一个元素相同，这个锁将会被永久锁定，无法再被旋转。
字符串 target 代表可以解锁的数字，你需要给出最小的旋转次数，如果无论如何不能解锁，返回 -1。

示例 1:
输入：deadends = ["0201","0101","0102","1212","2002"], target = "0202"
输出：6
解释：
可能的移动序列为 "0000" -> "1000" -> "1100" -> "1200" -> "1201" -> "1202" -> "0202"。
注意 "0000" -> "0001" -> "0002" -> "0102" -> "0202" 这样的序列是不能解锁的，
因为当拨动到 "0102" 时这个锁就会被锁定。
示例 2:
输入: deadends = ["8888"], target = "0009"
输出：1
解释：
把最后一位反向旋转一次即可 "0000" -> "0009"。
示例 3:
输入: deadends = ["8887","8889","8878","8898","8788","8988","7888","9888"], target = "8888"
输出：-1
解释：
无法旋转到目标数字且不被锁定。
示例 4:
输入: deadends = ["0000"], target = "8888"
输出：-1
提示：
死亡列表 deadends 的长度范围为 [1, 500]。
目标数字 target 不会在 deadends 之中。
每个 deadends 和 target 中的字符串的数字会在 10,000 个可能的情况 '0000' 到 '9999' 中产生。
来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/open-the-lock
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

from queue import Queue


class Solution:
    def openLock(self, deadends: list, target: str) -> int:
        deadends = set(deadends)  # in 操作在set中时间复杂度为O(1)
        if '0000' in deadends:
            return -1
        # -------------------------------BFS 开始----------------------------------
        # 初始化根节点
        q = Queue()
        q.put(('0000', 0))  # (当前节点值，转动步数)
        # 开始循环队列
        while not q.empty():
            # 取出一个节点
            node, step = q.get()
            # 放入周围的8个节点(每个轮上下拨一次)
            print(f'------{node}-------')
            for i in range(4):
                for add in (1, -1):
                    cur = node[:i] + str((int(node[i]) + add) % 10) + node[i + 1:]
                    if cur == target:
                        return step + 1
                    if not cur in deadends:
                        print('cur:', cur)
                        q.put((cur, step + 1))
                        deadends.add(cur)  # 避免重复搜索
        # -------------------------------------------------------------------------
        return -1


class Solution:
    def openLock(self, deadends: list, target: str) -> int:
        def plusone(s: str, j: int) -> str:
            ch = list(s)
            if ch[j] == '9':
                ch[j] = '0'
            else:
                ch[j] = str(int(ch[j]) + 1)
            return "".join(ch)

        def minusone(s: str, j: int) -> str:
            ch = list(s)
            if ch[j] == '0':
                ch[j] = '9'
            else:
                ch[j] = str(int(ch[j]) - 1)
            return "".join(ch)

        deads = set(deadends)
        visited = set()
        queue = []
        step = 0
        queue.append(("0000", step))
        visited.add("0000")
        while queue:
            cur, step = queue.pop(0)
            if cur in deads:
                continue
            if cur == target:
                return step

            for j in range(4):
                up = plusone(cur, j)
                if up not in visited:
                    queue.append((up, step + 1))
                    visited.add(up)

                down = minusone(cur, j)
                if down not in visited:
                    queue.append((down, step + 1))
                    visited.add(down)
        return -1


import collections


class Solution:
    def openLock(self, deadends: list, target: str) -> int:
        deadends_set = set(deadends)
        if '0000' in deadends: return -1
        # 对于每个数字，他下一步可以变的数值
        LUT = {'0': '91', '1': '02', '2': '13', '3': '24', '4': '35', '5': '46',
               '6': '57', '7': '68', '8': '79', '9': '80'}
        queue = collections.deque()
        # 存入密码和当前层
        queue.append(('0000', 0))
        # 防止重复
        visited = set()
        visited.add('0000')
        while queue:
            # 取出密码和当前层
            node, step = queue.popleft()
            if node == target:
                return step
            for i, c in enumerate(node):
                for char in LUT[c]:
                    new = node[:i] + char + node[i + 1:]
                    if new not in visited and new not in deadends_set:
                        queue.append((new, step + 1))
                        visited.add(new)
        return -1


class Solution:
    def openLock(self, deadends: list, target: str) -> int:
        # 转为集合,O(1)查找
        deadends = set(deadends)
        # 特判
        if '0000' in deadends:
            return -1
        if '0000' in target:
            return 0
        # 起始节点
        left = set()
        left.add('0000')
        # 结束节点
        right = set()
        right.add(target)
        step = 0

        while left:
            next_level = set()
            # 每次都搜索节点较少的一边
            if len(left) > len(right):
                left, right = right, left
            # 普通的bfs
            for node in left:
                for i in range(4):
                    for add in (1, -1):
                        cur = node[:i] + str((int(node[i]) + add) % 10) + node[i + 1:]
                        # 如果当前节点的下一个节点,在另一边的节点中了,那么说明再往下走一层,就可以连通,也就是可以解锁了.
                        if cur in right:
                            return step + 1
                        # 将节点加入下一层要加入的节点中,将deadends作为我们的visited数组..
                        if cur not in deadends:
                            next_level.add(cur)
                            deadends.add(cur)
            # 每次走到下一层,步数都要+1
            step += 1
            left = next_level
        return -1


deadends = ["0201", "0101", "0102", "1212", "2002"]
target = "0202"

s = Solution()
print(s.openLock(deadends, target))
