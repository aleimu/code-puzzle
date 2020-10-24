__doc__ = "数组原地翻转"

arr = [x for x in range(10)]


def reverse(arr: list) -> list:
    i = 0
    j = len(arr)
    while i < j / 2:
        arr[i], arr[j - 1 - i] = arr[j - 1 - i], arr[i]
        i += 1  # 也可以
        # i = i + 1 可以
        # i = +1    不支持c语法,这就是i等于正1


print("before:", arr)
reverse(arr)
print("after:", arr)
