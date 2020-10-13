__doc__ = '起点->终点 的广度优先搜索'


# 图算法 -- 广度优先搜搜 -- BFS -- 队列（先进先出）
# 1.利用队列实现
# 2.从源节点开始依次按照宽度进队列，然后弹出
# 3.每弹出一个节点，就把该节点所有没有进过队列的邻接点放入队列
# 4.直到比遍历到的点是终点或队列变空
# 5.BFS 找到的路径一定是最短的，借助队列做到一次一步「齐头并进」，是可以在不遍历完整棵树的条件下找到最短距离的,但代价就是空间复杂度比 DFS 大很多.

def BFS(graph, start, end):
    queue = []  # 核心数据结构,模拟队列
    queue.append(start)  # 将起点加入队列
    visited = set()  # 避免走回头路
    visited.add(start)
    step = 0  # 记录扩散的步数
    while queue:
        vertex = queue.pop(0)
        print('now:', vertex)
        if vertex == end:  # 判断是否已找到终点
            print('find end:', vertex)
            break
        nodes = graph[vertex]
        for w in nodes:
            if w not in visited:
                print('--> ', w)
                queue.append(w)  # 将没有访问过的加入下一次遍历
                visited.add(w)
                step += 1
    print('BFS cost steps:', step)


graph = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D", "F", "E"],
    "D": ["B", "C", "E", "F"],
    "E": ["C", "D"],
    "F": ["D"]
}
print("-----BFS-----")
BFS(graph, "A", "F")
