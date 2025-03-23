from collections import deque


def is_valid(state, total_m, total_c):
    # state: (m_left, c_left, boat_side)
    m_left, c_left, _ = state
    m_right = total_m - m_left
    c_right = total_c - c_left

    # Check for negative numbers or numbers exceeding total
    if m_left < 0 or c_left < 0 or m_left > total_m or c_left > total_c:
        return False

    # On left bank: if there are missionaries, they should not be outnumbered
    if m_left > 0 and m_left < c_left:
        return False
    # On right bank: if there are missionaries, they should not be outnumbered
    if m_right > 0 and m_right < c_right:
        return False

    return True


def get_successors(state, total_m, total_c, boat_capacity):
    successors = []
    m_left, c_left, boat = state
    # if boat is on left bank, move from left to right; else vice versa
    direction = -1 if boat == 0 else 1

    # Try all possible moves with 1 to boat_capacity people
    for m in range(boat_capacity + 1):
        for c in range(boat_capacity + 1):
            if m + c == 0 or m + c > boat_capacity:
                continue
            # Depending on boat side, subtract or add the numbers
            if boat == 0:
                new_state = (m_left - m, c_left - c, 1)
            else:
                new_state = (m_left + m, c_left + c, 0)
            if is_valid(new_state, total_m, total_c):
                successors.append(((m, c), new_state))
    return successors


def bfs(initial_state, total_m, total_c, boat_capacity):
    # Queue holds tuples: (state, path) where path is a list of (move, state) tuples
    queue = deque()
    queue.append((initial_state, []))
    visited = set()
    visited.add(initial_state)

    while queue:
        state, path = queue.popleft()
        # Check if goal reached: all on the right bank
        if state[0] == 0 and state[1] == 0 and state[2] == 1:
            return path

        for move, next_state in get_successors(state, total_m, total_c, boat_capacity):
            if next_state not in visited:
                visited.add(next_state)
                # Append move details and next state to path
                queue.append((next_state, path + [(move, next_state)]))
    return None


def print_solution(path, total_m, total_c):
    if not path:
        print("No solution found.")
        return

    state_desc = lambda \
        s: f"(Missionaries left: {s[0]}, Cannibals left: {s[1]}, Boat on: {'Left' if s[2] == 0 else 'Right'})"
    # Print the initial state
    initial_state = (total_m, total_c, 0)
    print("Initial state:", state_desc(initial_state))
    for i, (move, state) in enumerate(path, start=1):
        m_move, c_move = move
        direction = "-> Right" if state[2] == 1 else "-> Left"
        print(f"Step {i}: Move {m_move} missionary(ies) and {c_move} cannibal(s) {direction}.")
        print("         New state:", state_desc(state))


def main():
    print("Missionaries and Cannibals Problem Solver")

    # Take user input
    try:
        total_m = int(input("Enter the number of missionaries: "))
        total_c = int(input("Enter the number of cannibals: "))
        boat_capacity = int(input("Enter the boat capacity: "))
    except ValueError:
        print("Invalid input. Please enter integers only.")
        return

    # Basic feasibility check: At least one person must be in the boat.
    if boat_capacity < 1:
        print("Boat capacity must be at least 1.")
        return

    initial_state = (total_m, total_c, 0)
    solution = bfs(initial_state, total_m, total_c, boat_capacity)

    if solution:
        print("\nSolution found!\n")
        print_solution(solution, total_m, total_c)
    else:
        print("\nNo solution exists for the given input.")


if __name__ == "__main__":
    main()
