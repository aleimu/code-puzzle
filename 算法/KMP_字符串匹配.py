__doc__ = """
https://zhuanlan.zhihu.com/p/76348091
KMP算法是一种字符串匹配算法, 可以在 O(n+m) 的时间复杂度内实现两个字符串的匹配。
字符串 P 是否为字符串 S 的子串？如果是, 它出现在 S 的哪些位置？其中 S 称为主串；P 称为模式串

核心思想: 
1.在暴力匹配的基础上优化匹配步骤
2.寻找子模式串规律,可以帮助主串跳过一定不能匹配的位置
3.遍历子串用到了双指针和递推关系,遍历主串也是双指针和递推关系,都是记忆了前面的状态,辅助之后的判断

"""


# 最朴素的字符串匹配算法 Brute-Force
# 枚举 i = 0, 1, 2 ... , len(S)-len(P)
# 将 S[i : i+len(P)] 与 P 作比较。如果一致, 则找到了一个匹配

def bruteForce(s, p):
    """暴力遍历,一步一步往前试,复杂度O(m*n)"""
    sl = len(s)
    pl = len(p)
    for i in range(sl - pl + 1):
        if s[i:i + pl] == p:
            print(i)


"""
定义:
    "前缀" 指除了最后一个字符以外, 一个字符串的全部头部组合；
    "后缀" 指除了第一个字符以外, 一个字符串的全部尾部组合.

下面再以"ABCDABD"为例, 进行介绍：
    ---　"A"的前缀和后缀都为空集, 共有元素的长度为0；
    ---　"AB"的前缀为[A], 后缀为[B], 共有元素的长度为0；
    ---　"ABC"的前缀为[A, AB], 后缀为[BC, C], 共有元素的长度0；
    ---　"ABCD"的前缀为[A, AB, ABC], 后缀为[BCD, CD, D], 共有元素的长度为0；
    ---　"ABCDA"的前缀为[A, AB, ABC, ABCD], 后缀为[BCDA, CDA, DA, A], 共有元素为"A", 长度为1；
    ---　"ABCDAB"的前缀为[A, AB, ABC, ABCD, ABCDA], 后缀为[BCDAB, CDAB, DAB, AB, B], 共有元素为"AB", 长度为2；
    ---　"ABCDABD"的前缀为[A, AB, ABC, ABCD, ABCDA, ABCDAB], 后缀为[BCDABD, CDABD, DABD, ABD, BD, D], 共有元素的长度为0。
分别取出长度组成列表 [0, 0, 0, 0, 1, 2, 0]
"""


# 模式匹配表
def partial_table(p):
    """partial_table("ABCDABD") -> [0, 0, 0, 0, 1, 2, 0]"""
    prefix = set()  # 前缀合集
    ret = [0]  # 第一个字符A,不满足取前缀后缀的条件,下面for中也跳过了第一个字符的检查
    for i in range(1, len(p)):
        prefix.add(p[:i])  # 前缀
        postfix = {p[j:i + 1] for j in range(1, i + 1)}  # 后缀
        ret.append(len((prefix & postfix or {''}).pop()))  # 找到前后缀相同的子串并取长度
    return ret


def partial_table(p):
    """最长前后缀相同的字符位数---双指针法---递推法---模式串中寻找最长前后缀的推导过程中也包含递进关系"""
    n = len(p)  # 整个字符串长度
    j = 0  # 前缀匹配指向
    i = 1  # 后缀匹配指向
    result_list = [0] * n
    while i < n:
        print('-----------------------------------------')
        print(f"i:{i}, j:{j}, result_list:{result_list}")
        if p[j] != p[i]:  # 比较不相等
            if j == 0:  # 此时比较的是前缀第一个字符
                result_list[i] = 0  # 值为０
                i += 1  # 向后移动
            else:  # 比较不相等,将j值设置为ｊ前一位的result_list中的值, 为了在之前匹配到的子串中找到最长相同前后缀
                j = result_list[j - 1]
        else:  # 相等则继续比较下一位
            result_list[i] = j + 1
            j = j + 1
            i = i + 1
        print(f"i:{i}, j:{j}, result_list:{result_list}")
    return result_list


# 如果 S[i : i+len(P)] 与 P 的匹配是在第 r 个位置失败的, 那么从 S[i] 开始的 (r-1) 个连续字符, 一定与 P 的前 (r-1) 个字符一模一样
# 利用上次失败的信息,跳过接下来不可能成功的尝试
def kmp_match(s, p):
    m = len(s)
    n = len(p)
    cur = 0  # 起始指针cur
    table = partial_table(p)
    while cur <= m - n:  # 只去匹配前m-n个
        for i in range(n):
            if s[i + cur] != p[i]:
                cur += max(i - table[i - 1], 1)  # 有了部分匹配表,我们不只是单纯的1位1位往右移,可以一次移动多位
                break
        else:  # for 循环中, 如果没有从任何一个 break 中退出, 则会执行和 for 对应的 else
            # 只要从 break 中退出了, 则 else 部分不执行。
            return True
    return False


def kmp(s, p):
    """kmp算法,s是字符串，p是模式字符串，返回值为匹配到的第一个字符串的第一个字符的索引，没匹配到返回-1"""
    s_length = len(s)
    p_length = len(p)
    i = 0  # 指向s
    j = 0  # 指向p
    next = partial_table(p)
    while i < s_length:
        if s[i] == p[j]:  # 对应字符相同
            i += 1
            j += 1
            if j >= p_length:  # 完全匹配
                return i - p_length
        elif s[i] != p[j]:  # 不相同
            if j == 0:  # 与模式比较的是模式的第一个字符
                i += 1
            else:  # 取模式当前字符之前最长相同前后缀的前缀的后一个字符继续比较
                j = next[j]
    if i == s_length:  # 没有找到完全匹配的子串
        return -1


s = '111234562348031123341231235342123123123'
p = '123123'
# bruteForce(s, p)
# print(kmp_match(s, p))


# print(partial_table("ABCDABD"))
# print(kmp_match("BBC ABCDAB ABCDABCDABDE", "ABCDABD"))

# print(partial_table(p))
print(partial_table("ABCDABDCABC"))
