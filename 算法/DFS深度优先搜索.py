__doc__ = '起点->终点 的深度优先搜索'


# 图算法 -- 深度优先搜搜 -- DFS -- 栈（先进后出）
# 1.利用栈实现
# 2.从源节点开始把节点按照深度放入栈，然后弹出
# 3.每弹出一个点，把该节点下一个没有进过栈的邻接点放入栈
# 4.直到比遍历到的点是终点或队列变空

def DFS(graph, start, end):
    stack = [start]
    visited = set()
    step = 0  # 记录扩散的步数
    while stack:
        vertex = stack.pop()
        if vertex == end:
            print('find end:', vertex)
            break
        print('now:', vertex)
        if vertex not in visited:
            visited.add(vertex)
            for w in graph[vertex]:
                if w not in visited:
                    print('--> ', w)
                    stack.append(w)
                    step += 1
    print('DFS cost steps:', step)


graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D", "E"],
    "D": ["B", "C", "E", "F"],
    "E": ["C", "D"],
    "F": ["D"]
}
print("-----DFS-----")
DFS(graph, "A", "F")
