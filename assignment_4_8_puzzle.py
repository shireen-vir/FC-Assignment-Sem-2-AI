import heapq
from copy import deepcopy
GOAL_STATE = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

MOVES = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Left': (0, -1),
    'Right': (0, 1)
}

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x = (value - 1) // 3
                goal_y = (value - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def get_neighbors(state):

    x = y = None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = i, j
                break
        if x is not None:
            break

    neighbors = []
    for move, (dx, dy) in MOVES.items():
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = deepcopy(state)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append((new_state, move))
    return neighbors

def state_to_tuple(state):
    return tuple(item for row in state for item in row)

def a_star(start_state):
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start_state), 0, start_state, []))
    closed_set = set()

    while open_list:
        priority, cost, current_state, path = heapq.heappop(open_list)

        if current_state == GOAL_STATE:
            return path

        state_key = state_to_tuple(current_state)
        if state_key in closed_set:
            continue
        closed_set.add(state_key)

        for neighbor, move in get_neighbors(current_state):
            neighbor_key = state_to_tuple(neighbor)
            if neighbor_key in closed_set:
                continue
            new_cost = cost + 1
            heuristic = manhattan_distance(neighbor)
            new_priority = new_cost + heuristic
            new_path = path + [(neighbor, move)]
            heapq.heappush(open_list, (new_priority, new_cost, neighbor, new_path))

    return None

def print_state(state):
    for row in state:
        print(" ".join(str(num) if num != 0 else " " for num in row))
    print()

def main():
    print("Enter the initial state of the 8-puzzle, use 0 to represent the blank space.")
    print("Enter 9 numbers (separated by space or newline).")
    try:
        raw_input = input("Enter the numbers: ")
        numbers = list(map(int, raw_input.strip().split()))
        if len(numbers) != 9:
            raise ValueError("Please enter exactly 9 numbers.")
        start_state = [numbers[i*3:(i+1)*3] for i in range(3)]
    except Exception as e:
        print("Invalid input:", e)
        return

    print("\nInitial state:")
    print_state(start_state)

    result = a_star(start_state)
    if result is None:
        print("No solution found for the given puzzle.")
    else:
        print("Solution found in", len(result), "moves:")
        move_number = 1
        for state, move in result:
            print(f"Move {move_number}: {move}")
            print_state(state)
            move_number += 1

if __name__ == "__main__":
    main()
