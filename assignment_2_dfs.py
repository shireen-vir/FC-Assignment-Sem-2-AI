class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = {i: [] for i in range(vertices)}

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def dfs(self, start):
        visited = [False] * self.V
        stack = [start]

        print("Depth-First Traversal starting from node", start, ":")

        while stack:
            node = stack.pop()

            if not visited[node]:
                print(node, end=" ")
                visited[node] = True
                for neighbor in reversed(self.graph[node]):
                    if not visited[neighbor]:
                        stack.append(neighbor)

def take_input():
    vertices = int(input("Enter the number of vertices: "))
    g = Graph(vertices)
    edges = int(input("Enter the number of edges: "))
    for _ in range(edges):
        u, v = map(int, input("Enter edge (u v): ").split())
        g.add_edge(u, v)
    start = int(input("Enter the starting node for DFS: "))

    return g, start


if __name__ == "__main__":
    graph, start_node = take_input()
    graph.dfs(start_node)
