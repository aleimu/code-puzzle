__doc__ = "一些复杂点的列表推导"

s = ['son', 'abc', 'pro', 'bro']
b = ['son', 'bro']
c = ['pro', 'quo']

print([i if i % 2 == 0 else 'qi' for i in range(10)])
print([s.index(item) if item in b else s.index(item) + 10 for item in s if item in c])
print([i if item in b else i + 10 if item in c else None for i, item in enumerate(s) if item in b or item in c])
print([(x, y, z) for x in range(5) if x > 2 for y in range(6) if y > 3 for z in range(10) if z > 4])
print(['零' if i == 0 else '三' if i == 3 else '五' if i == 5 else i for i in range(20)])
