import random
import string

# range has to be 10 or less
matrix_size = 10
ships = 20

board = [['.' for col in range(matrix_size)] for row in range(matrix_size)]

# fill the board with 10 random stars
positions = set()
while len(positions) < ships:
    coord = (random.randint(0, matrix_size-1), random.randint(0, matrix_size-1))
    positions.add(coord)

for x,y in positions:
    board[x][y] = "o"


top_labels = range(matrix_size)
side_labels = string.ascii_uppercase[:matrix_size]

print(" ", *[*top_labels])
for row in range(matrix_size):
    print(side_labels[row], end=" ")
    print(*board[row])