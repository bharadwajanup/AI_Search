import Queue
import random
global INT
def print_move():
    return 0

def find_num(board, num):
    for i in range(4):
        for j in range(4):
            if board[i][j] == num:
                return [i,j]

# Compact heuristic
def heuristic(s, index):
    if index == 1:
        return heuristic1(s)
    elif index == 2:
        return heuristic2(s)
    else:
        return heuristic3(s)

# Steps to move from current to final
def heuristic1(s):
    # index is the calculated difference
    # number in list is the actural difference
    diff_adjust = [0, 1, 2, 1]
    sum = 0
    for num in range(1, 16):
        x = (num-1)/4
        y = (num-1)%4
        [xp, yp] = find_num(s, num)
        diffx = diff_adjust[abs(x-xp)]
        diffy = diff_adjust[abs(y-yp)]
        sum += diffx + diffy
    return sum

# Num of misplaced tiles
def heuristic2(s):
    sum = 0
    for num in range (1, 16):
        x = (num-1)/4
        y = (num-1)%4
        if s[x][y] != num:
            sum+=1
    return sum

# Inversion plus the blank row number of a particular board
def blank_plus_inversion(s):
    sum = 0
    [x0, y0] = find_num(s, 0)
    sum += x0
    for num in range(1, 16):
        [xp, yp] = find_num(s, num)
        for i in range(yp+1, 4):
            if s[xp][i] < num and s[xp][i] != 0:
                sum += 1
        for i in range(xp+1, 4):
            for j in range(4):
                if s[i][j] < num and s[i][j] != 0:
                    sum += 1
    return sum

# Change is made directly on the board that is passed on
def change_position(board, move):
    [x0, y0] = find_num(board, 0)
    if move == 'U':
        x = (x0+1)%4
        y = y0
    elif move == 'D':
        x = (x0-1)%4
        y = y0
    elif move == 'L':
        x = x0
        y = (y0+1)%4
    else:
        x = x0
        y = (y0-1)%4

    board_copy = [[0] * 4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            board_copy[i][j] = board[i][j]
    board_copy[x0][y0] = board[x][y]
    board_copy[x][y] = 0
    return board_copy

def change_position_back (state):
    board = state[1]
    move = state[2]
    [x0, y0] = find_num(board, 0)
    if move == 'D':
        x = (x0+1)%4
        y = y0
    elif move == 'U':
        x = (x0-1)%4
        y = y0
    elif move == 'R':
        x = x0
        y = (y0+1)%4
    else:
        x = x0
        y = (y0-1)%4

    board_copy = [[0] * 4 for i in range(4)]
    for i in range(4):
        for j in range(4):
            board_copy[i][j] = board[i][j]
    board_copy[x0][y0] = board[x][y]
    board_copy[x][y] = 0
    return board_copy

def successors(state):
    s = state[1]
    currentCost = state[0] + 1 - heuristic(s, INT)
    moveList = ['U', 'D', 'L', 'R']
    returnList = []

    if len(processed_states) % 50000 == 0:
        print "currentCost is ", currentCost
        print "heuristic cost is ", heuristic(s, INT)

    for i in range(4):
        s_p = change_position(s, moveList[i])
        hCost = heuristic(s_p, INT)
        returnList.append((currentCost+hCost, s_p, moveList[i]))
    return returnList
    #return [[(currentCost+heuristic(s_p, INT), s_p, moveList[i])] for s_p in [change_position(s, moveList[i]) for i in range(4)]]

def solve15(initial_board):
    fringe = Queue.PriorityQueue()
    fringe.put((heuristic(initial_board, INT), initial_board, None))
    while not fringe.empty():
        state = fringe.get()
        s = state[1]
        move = state[2]
        processed_states.append(state)
        if s == final_board:
            return (s)
        for state_p in successors(state):
           fringe.put(state_p)
    return False

def find_route(states):
    route = []
    final_state = states.pop()
    route.append(final_state[2])
    temp_state = states.pop()
    previous_board = change_position_back(temp_state)
    while len(states) > 0:
        if temp_state[1] == previous_board:
            route.append(temp_state[2])
            previous_board = change_position_back(temp_state)
        else:
            temp_state = states.pop()
    route.reverse()
    return route

# Read in the initial board file
#f = open('input-board.txt', 'r')
initial_board = [[0] * 4 for i in range(4)]
#for i in range(4):
#    line = f.readline()
#    j = 0
#    for s in line.split():
#        initial_board[i][j] = int(s)
#        j += 1
#f.close()

# following code generate a random initial_board
sample_board = range(16)
random.shuffle(sample_board)
k = 0
for i in range(4):
    for j in range(4):
        initial_board[i][j] = sample_board[k]
        k += 1

print "The initial board is " 
print initial_board
board_feature = blank_plus_inversion(initial_board)
print "The blank row plus inversion of initial board is %d" %board_feature

if board_feature%2 == 0:
    print "This initial board is unsolvable because the blank row plus the inversion is an odd number"
else:
    # Create the final state
    final_board = [[0] * 4 for i in range(4)]
    num = 1
    for i in range(4):
        for j in range(4):
            final_board[i][j] = num
            num += 1
            final_board[3][3] = 0

    # Test different heuristic function
    for INT in range(1, 3):
        processed_states = []
        print "Using heuristic function %d to find the final board:" %INT
        solution = solve15(initial_board)
        print solution
        print "%d states are evaluated in this process" %len(processed_states)
        print "The solution path is "
        print find_route(processed_states)
