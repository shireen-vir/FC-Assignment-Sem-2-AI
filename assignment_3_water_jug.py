from collections import deque

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def water_jug_bfs(x, y, d):
    if d > max(x, y) or d % gcd(x, y) != 0:
        return "No solution exists"

    queue = deque([(0, 0)])
    visited = set()
    visited.add((0, 0))

    parent_map = {}  # (jug1, jug2) -> parent state for path reconstruction
    while queue:
        jug1, jug2 = queue.popleft()
        if jug1 == d or jug2 == d:
            steps = []
            while (jug1, jug2) != (0, 0):
                steps.append((jug1, jug2))
                jug1, jug2 = parent_map[(jug1, jug2)]
            steps.append((0, 0))
            steps.reverse()
            return steps

        # Possible operations
        possible_states = [
            (x, jug2),
            (jug1, y),
            (0, jug2),
            (jug1, 0),
            (jug1 - min(jug1, y - jug2), jug2 + min(jug1, y - jug2)),
            (jug1 + min(x - jug1, jug2), jug2 - min(x - jug1, jug2)),
        ]

        # Process each possible state
        for state in possible_states:
            if state not in visited:
                visited.add(state)
                queue.append(state)
                parent_map[state] = (jug1, jug2)

    return "No solution exists"

def print_steps(steps):
    print("Solution steps:")
    for step in steps:
        print(f"Jug 1: {step[0]}, Jug 2: {step[1]}")

if __name__ == "__main__":
    x = int(input("Enter the capacity of Jug 1: "))
    y = int(input("Enter the capacity of Jug 2: "))
    d = int(input("Enter the desired amount of water: "))

    result = water_jug_bfs(x, y, d)

    if isinstance(result, str):  # No solution
        print(result)
    else:
        print_steps(result)
