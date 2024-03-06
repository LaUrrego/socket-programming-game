import random
import string
import os
from typing import List, Tuple

class Battleship():
    # size range is 10 or less
    MATRIX_SIZE = 10
    # should be half the size or less
    SHIPS = 20
    SHIP_PIECE = "o"
    KEYS = {letter:index for index, letter in enumerate(string.ascii_lowercase[:MATRIX_SIZE])}


    def __init__(self, turn) -> None:
        self._board = self._create_board()
        self._ship_count = self.SHIPS
        # turn 1 or 2
        self.turn = turn
    
    def _create_board(self) -> List[List[str]]:
        """
        Initialize board and set with randomized battleships
        """
        board = [['.' for col in range(self.MATRIX_SIZE)] for row in range(self.MATRIX_SIZE)]
        # fill the board with random ships
        positions = set()
        while len(positions) < self.SHIPS:
            coord = (random.randint(0, self.MATRIX_SIZE-1), random.randint(0, self.MATRIX_SIZE-1))
            positions.add(coord)

        for x,y in positions:
            board[x][y] = "o"
        
        return board
    
    def _print_board(self) -> None:
        """
        Stylized console printout of the current board
        """
        top_labels = range(self.MATRIX_SIZE)
        side_labels = string.ascii_uppercase[:self.MATRIX_SIZE]
        print(" ", *[*top_labels])
        for row in range(self.MATRIX_SIZE):
            print(side_labels[row], end=" ")
            print(*self._board[row])

    def _game_over(self) -> bool:
        """
        Checks whether the game is over
        """
        return self.ship_count == 0
    
    def _opps_turn(self, xpos, ypos) -> bool:
        """
        Conducts the opponents turn and confirm's whether it was a hit or not
        """
        xnum = self.KEYS[xpos]
        ynum = int(ypos)

        if self._board[xnum][ynum] == self.SHIP_PIECE:
            self._board[xnum][ynum] = "x" 
            self._ship_count -= 1
            print(f"Direct hit on ship {xpos},{ypos}! ")
            return True
        self._board[xnum][ynum] = "x"
        print("It's a miss!")
        return False

        
    def _your_turn(self, xpos, ypos) -> Tuple:
        xnum = self.KEYS[xpos]
        ynum = int(ypos)
        if not ((0 <= xnum < self.MATRIX_SIZE) and (0<= ynum < self.MATRIX_SIZE)):
            print(f"Enter valid positions! Try again.")
            return False, -1, -1
        return True, xpos, ypos
    
    def play_game(self):
        # if it's your turn, you can start otherwise:
        
        # check for opponents turn

        # do your turn
        pass



        
        


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
print(side_labels)

print(" ", *[*top_labels])
for row in range(matrix_size):
    print(side_labels[row], end=" ")
    print(*board[row])

KEYS = {letter:index for index, letter in enumerate(string.ascii_lowercase[:matrix_size])}
print(KEYS)