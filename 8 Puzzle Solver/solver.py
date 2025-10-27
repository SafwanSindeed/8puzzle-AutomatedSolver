from heapq import heappush, heappop

Goal = '012345678'  # WE WANT THIS // 0 indicates the BLANK SPACE
Board_Size = 3      # Grid Size

def show_board(state):
    for i in range(0, 9, 3):
        print(''.join(state[i:i+3]))
    print()

def check_solvable(state):
    nums = [int(x) for x in state if x != '0']
    inversions = 0

    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]: 
                inversions += 1
    return inversions % 2 == 0

def estimate_distance(state):
    total = 0  # if the total heurisitc disrtance form the goal states is 0 that mean the currernt board is the goal state

    for index, char in enumerate(state):
        if char == '0':
            continue
        title = int(char)

        current_row, current_colum = divmod(index, Board_Size)   # current randomly generated board state 
        goal_row, goal_colum = divmod(title, Board_Size)
        total += abs(current_row - goal_row) + abs(current_colum - goal_colum)
    return total

def possible_moves(state):
    moves = []
    zero = state.index('0')  
    row, colum = divmod(zero, Board_Size)  # changes index values into rows and colums

    def swap(new_zero, direction):
        s = list(state)
        s[zero], s[new_zero] = s[new_zero], s[zero]  # swaps 'Two pointers'
        moves.append((''.join(s), direction))  # NEW BOARD

    # Boundaries of the Board and Allowable legal moves
    if row > 0: swap(zero - 3, 'Up')
    if row < 2: swap(zero + 3, 'Down')
    if colum > 0: swap(zero - 1, 'Left')
    if colum < 2: swap(zero + 1, 'Right')

    return moves

def solve_puzzle(start):
    if start == Goal:           # Lucky LOL
        return [start], []
    if not check_solvable(start):
        return None, None

    front = []                            # priority queue
    g_costs = {start: 0}                     
    heappush(front, (estimate_distance(start), 0, start))
    came_from = {start: (None, None)}       

    while front:
        # Pop the state with lowest f cost
        _, g, state = heappop(front)

        if state == Goal:
            # Reconstruct path from goal back to start
            path, moves = [], []
            while state:
                parent, move = came_from[state]
                path.append(state)
                if move:
                    moves.append(move)
                state = parent
            return path[::-1], moves[::-1]   

        # Explore all possible next boards
        for next_state, move in possible_moves(state):
            new_cost = g + 1 

            # If new cost is better, update and push to front
            if next_state not in g_costs or new_cost < g_costs[next_state]:
                g_costs[next_state] = new_cost
                f = new_cost + estimate_distance(next_state)
                heappush(front, (f, new_cost, next_state))
                came_from[next_state] = (state, move)

    return None, None 

start = '724506831'  # TESTCASE
if check_solvable(start):
    path, moves = solve_puzzle(start)
    if path:
        print("Solved in", len(moves), "moves!\n")
        for step in path:
            show_board(step)
    else:
        print("No solution found.")
else:
    print("This puzzle is not solvable.")
