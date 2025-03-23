from collections import deque


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = {i: [] for i in range(vertices)}

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bfs(self, start):
        visited = [False] * self.V
        queue = deque([start])
        visited[start] = True

        print("Breadth-First Traversal starting from node", start, ":")
        while queue:
            node = queue.popleft()
            print(node, end=" ")

            for neighbor in self.graph[node]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True


def take_input():
    vertices = int(input("Enter the number of vertices: "))
    g = Graph(vertices)
    edges = int(input("Enter the number of edges: "))
    for _ in range(edges):
        u, v = map(int, input("Enter edge (u v): ").split())
        g.add_edge(u, v)
    start = int(input("Enter the starting node for BFS: "))

    return g, start

if __name__ == "__main__":
    graph, start_node = take_input()
    graph.bfs(start_node)
