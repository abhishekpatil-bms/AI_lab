import random

def conflicts(state):
    count = 0
    for i in range(4):
        for j in range(i + 1, 4):
            # same column or same diagonal
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                count += 1
    return count

def print_board(state):
    for i in range(4):
        row = ["Q" if state[i] == j else "." for j in range(4)]
        print(" ".join(row))
    print()

def hill_climbing():
    state = [random.randint(0, 3) for _ in range(4)]
    current_conflicts = conflicts(state)

    while True:
        best_state = state
        best_conflicts = current_conflicts

        # Try moving each queen to every other column
        for row in range(4):
            for col in range(4):
                if col == state[row]:
                    continue
                new_state = state.copy()
                new_state[row] = col
                new_conflicts = conflicts(new_state)

                if new_conflicts < best_conflicts:
                    best_conflicts = new_conflicts
                    best_state = new_state

        # If no improvement, stop
        print("State space now:")
        print_board(state)
        print("no of conflicts=",best_conflicts,"\n")
        if best_conflicts == current_conflicts:
            break

        # Update to new better state
        state = best_state
        current_conflicts = best_conflicts

        # Stop early if solved
        if current_conflicts == 0:
            break

    return state, current_conflicts

# --- Run the 4-Queens Hill Climbing ---
solution, c = hill_climbing()
print_board(solution)

if c == 0:
    print("Found a valid 4-Queens solution!")
else:
    print("Stuck in local minimum (", c, "conflicts )")
