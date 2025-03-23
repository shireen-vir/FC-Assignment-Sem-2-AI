import heapq
from copy import deepcopy

# Define the goal state for the 8-puzzle
GOAL_STATE = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

# Define possible moves: up, down, left, right
MOVES = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Left': (0, -1),
    'Right': (0, 1)
}

def manhattan_distance(state):
    """Calculate the Manhattan distance heuristic for a given state."""
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
    """Generate all valid neighbor states from the current state."""
    # Find the blank (0) position
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
        # Check if the new position is within bounds
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = deepcopy(state)
            # Swap the blank with the adjacent number (fixed swap)
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            neighbors.append((new_state, move))
    return neighbors

def state_to_tuple(state):
    """Convert 2D state list to a tuple to use it in sets and as dict keys."""
    return tuple(item for row in state for item in row)

def a_star(start_state):
    """Perform the A* search to solve the puzzle."""
    # Priority queue element: (priority, cost, state, path)
    # where path is a list of (state, move) pairs leading to this state
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start_state), 0, start_state, []))
    closed_set = set()

    while open_list:
        priority, cost, current_state, path = heapq.heappop(open_list)

        if current_state == GOAL_STATE:
            return path  # Found solution; path is a list of moves

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

    return None  # No solution found

def print_state(state):
    """Helper function to print a state in a readable format."""
    for row in state:
        print(" ".join(str(num) if num != 0 else " " for num in row))
    print()

def main():
    print("Enter the initial state of the 8-puzzle, use 0 to represent the blank space.")
    print("Enter 9 numbers (separated by space or newline).")
    try:
        # Read input from the user
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
