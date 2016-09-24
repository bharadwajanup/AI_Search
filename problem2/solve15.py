# run the following command: python solve15.py [input-board-filename]
# eg. python solve15.py input-board.txt

'''

1. Precisely defining the state space, the successor function, the edge weights, and (if applicable) the heuristic function(s) you designed, including an argument for why they are admissible?
1) The number of whols state space is 16!. Each state is a permutation of number 0 to 15 on the board. The goal state is the tiles in an order of 1, 2, 3, ... 15.
2) Each state has four successor states which corresponds to move the tile up, down, left and right to the blank space.
3) The cost from one state to its successor state is uniform: just one move.
4) I used two heuristic function. The first is using the manhattan distance between the actual position of a tile and the position the tile will be on the goal state. The second heuristic function I use is the number of misplaced tiles in the initial board.

2. How your search algorithm works?
I used A* search to decrease the states to be searched. The first heuristic function using the manhattan distance works preety well which will find the result very quick. But the second heuristic function does not seem to work at all: it always reach the memory limits. By observing the search states of the second function, I barely see any improvemets compared on breadth first search.

3. More detail on the heuristic funtion.
1) Both heuristic function are obviously admissible. Because each move can only change the position of one tile, even the manhattan distance counts for the minimum moves needed to reach the goal state. Even though both functions are admissible, we can certainly tell that the first heuristic function, which explains why the first works better.
2) I tried to find out a better heuristic than the manhattan distance, because in general case if the manhattan distance is 2, it usually takes more than 2 steps to reach the goal positon. We can only move the tile towards the goal positon by one step and then moving the tile on the goal positon away also takes 2 steps and then move the tile to the goal positon. It is reasonable to infer that we can use bigger value for heuristic cost.
3) But if considering a special case in a 2 by 2 board, which has the following board state: 0, 3, 1, 2, we can see that the manhattan distance is 6 and the actural move needed is also 6. So it is hard to apply the rule in the general case. I also considered using the inversion as the heuristic funtion but it obviously is not admissible. So far the manhattan distance heuristic function is the best I can think of and it also works fine.

4. One big issue in this problem is that the state graph is divided into two groups. The even odd property of a feature number is the measure. This featrue number is the inversion plus the blank row number.
The mathmatic model of moving the tile can be simplifid as x crossing a list of [x1, x2, x3 ... xn]. The inversion inside this list will not change. If n is an odd number, the change of inversion after x moving to the tail will also be an odd number. Same applies if n is an even number.
With the above abstruction, the tile we move (which is the x above) will always cross enven number of tiles if moving horizontally which will not change the even odd property of the feature number. If moving vertically, x will always cross odd number of tiles. But if counting on the change of the blank row number, the feature number stays even or odd. So the state graph are divided into tow parts. Some initial board will never get to the goal board.
'''
import Queue
import random
import sys

global INT

# Find the position of a number on board
def find_num(board, num):
    for i in range(4):
        for j in range(4):
            if board[i][j] == num:
                return [i,j]
    return "Number not on board"

# Compact heuristic
def heuristic(s, index):
    if index == 1:
        return heuristic1(s)
    else:
        return heuristic2(s)

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

# Get the previous board state
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

# Successor function. Get the following 4 states.
def successors(state):
    s = state[1]
    currentCost = state[0] + 1 - heuristic(s, INT)
    moveList = ['U', 'D', 'L', 'R']
    returnList = []
    for i in range(4):
        s_p = change_position(s, moveList[i])
        hCost = heuristic(s_p, INT)
        returnList.append((currentCost+hCost, s_p, moveList[i]))
    return returnList

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

# Base on all the processed states to find the right move path.
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
f = open(sys.argv[1], 'r')
initial_board = [[0] * 4 for i in range(4)]
print sys.argv
for i in range(4):
    line = f.readline()
    j = 0
    for s in line.split():
        initial_board[i][j] = int(s)
        j += 1
f.close()

# following code generate a random initial_board
#sample_board = range(16)
#random.shuffle(sample_board)
#k = 0
#for i in range(4):
    #for j in range(4):
        #initial_board[i][j] = sample_board[k]
        #k += 1

print "The initial board is " 
print initial_board
board_feature = blank_plus_inversion(initial_board)
print "The blank row plus inversion of initial board is %d" %board_feature

if board_feature%2 == 0:
    print "This initial board is unsolvable because the blank row plus the inversion is an even number"
else:
    # Construct the final state
    final_board = [[0] * 4 for i in range(4)]
    num = 1
    for i in range(4):
        for j in range(4):
            final_board[i][j] = num
            num += 1
            final_board[3][3] = 0

    # Test different heuristic function
    for INT in range(1, 2):
        processed_states = []
        print "Using heuristic function %d to find the final board:" %INT
        solution = solve15(initial_board)
        print solution
        print "%d states are evaluated in this process" %len(processed_states)
        print "The solution path is "
        print find_route(processed_states)

