f = open('input-board.txt', 'r')
initial_board = [[0]*4 for i in range(4)]
for i in range(4):
    line = f.readline()
    j = 0
    for s in line.split():
        initial_board[i][j] = int(s)
        j += 1
f.close()
