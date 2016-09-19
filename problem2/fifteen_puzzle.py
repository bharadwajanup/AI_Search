import Queue
def print_move():
    return 0

def find_num(board, num):
    for i in range(4):
        for j in range(4):
            if board[i][j] == num:
                return [i,j]
def heuristic(s):
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

def successors(state):
    s = state[1]
    currentCost = state[0] + 1 - heuristic(s)
    moveList = ['U', 'D', 'L', 'R']
    returnList = []

    print "current route is " + str(currentCost-1)
    print "heuristic is " + str(heuristic(s))

    for i in range(4):
        s_p = change_position(s, moveList[i])
        hCost = heuristic(s_p)
        returnList.append((currentCost+hCost, s_p, moveList[i]))
    return returnList
    #return [[(currentCost+heuristic(s_p), s_p, moveList[i])] for s_p in [change_position(s, moveList[i]) for i in range(4)]]

def solve15(initial_board):
    fringe = Queue.PriorityQueue()
    fringe.put((heuristic(initial_board), initial_board, None))
    while not fringe.empty():
        state = fringe.get()
        s = state[1]
        move = state[2]

        print s

        if s == final_board:
            return (s)
        for state_p in successors(state):
           fringe.put(state_p)
    return False

# Read in the initial board file
f = open('input-board.txt', 'r')
initial_board = [[0] * 4 for i in range(4)]
for i in range(4):
    line = f.readline()
    j = 0
    for s in line.split():
        initial_board[i][j] = int(s)
        j += 1
f.close()

# Create the final state
final_board = [[0] * 4 for i in range(4)]
num = 1
for i in range(4):
    for j in range(4):
        final_board[i][j] = num
        num += 1
final_board[3][3] = 0

solution = solve15(initial_board)
print solution
#print_move()
