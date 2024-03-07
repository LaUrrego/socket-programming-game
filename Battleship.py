import random
import string
import os
from typing import List, Tuple
from Colors import ColorsBg, ColorsFg

class Battleship():
    # size range is 10 or less
    MATRIX_SIZE = 6
    # should be half the size or less
    SHIPS = 5
    SHIP_PIECE = "o"
    SHIP_COLOR = ColorsFg.cyan
    HIT_COLOR = ColorsFg.red
    RESET = ColorsFg.reset
    LOGO_COLOR = ColorsFg.orange
    PLAYER_COLOR= ColorsFg.orange
    SCORE_YOUR_SHIPS = ColorsFg.lightgreen
    SCORE_OPP_SHIPS = ColorsFg.lightred

    KEYS = {letter:index for index, letter in enumerate(string.ascii_uppercase[:MATRIX_SIZE])}


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
            for cell in self._board[row]:
                if cell == 'x':
                    print(f'{self.HIT_COLOR}{cell}{self.RESET}', end=" ")
                elif cell == self.SHIP_PIECE:
                    print(f'{self.SHIP_COLOR}{cell}{self.RESET}', end=" ")
                else:
                    print(cell, end=" ")
            print()

    def _game_over(self) -> bool:
        """
        Checks whether the game is over
        """
        return self._ship_count == 0
    
    def _opps_turn(self, xpos, ypos) -> Tuple[bool,str]:
        """
        Conducts the opponents turn and confirm's whether it was a hit or not
        """
        xnum = self.KEYS[xpos.upper()]
        ynum = int(ypos)

        if self._board[xnum][ynum] == self.SHIP_PIECE:
            self._board[xnum][ynum] = "x" 
            self._ship_count -= 1
            print(f"Direct hit on ship {xpos},{ypos}!")
            return True, f"Direct hit on ship {xpos},{ypos}!"
        self._board[xnum][ynum] = "x"
        print("It's a miss!")
        return False, "It's a miss!"

        
    def _your_turn(self, xpos, ypos) -> Tuple[bool,str,str]:
        """
        Current player's turn
        """
        xnum = self.KEYS[xpos.upper()]
        ynum = int(ypos)
        if not ((0 <= xnum < self.MATRIX_SIZE) and (0<= ynum < self.MATRIX_SIZE)):
            print("Enter valid positions! Try again.")
            return False, -1, -1
        return True, xpos, ypos

    def _logo(self) -> str:
        """
        Send out the intro game logo
        """
        message = f'\n#######################################\n{self.LOGO_COLOR}SHIP BATTLE{self.RESET}\nThe Un-Battleship!\nClient always goes first. To end the game and go back to chat, enter /q\nGuess where your opponents ship is by entering a row then column\nThe first to sink all their opponents ships wins!\nEnter y when ready.\nWaiting for client response\n#######################################\nWaiting for client response...\n'
        print(message)

    def send_receive_score(self, conn, rec_fn) -> None:
        """
        Function to create a dynamic score board
        """
        # send your score details
        score_message = f'{self._ship_count}'.encode('utf-8')
        score_header = f'{len(score_message):<4}'.encode('utf-8')
        conn.send(score_header + score_message)

        # receive their score details
        score = int(rec_fn(conn))
        score_board = f'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n| {self.PLAYER_COLOR}Player: {self.turn}{self.RESET}\n| Your Ships: {self.SCORE_YOUR_SHIPS}{self._ship_count}{self.RESET}\n| Opponent Ships: {self.SCORE_OPP_SHIPS}{score}{self.RESET}\n| Hit Count: {self.SCORE_YOUR_SHIPS}{self.SHIPS - score}{self.RESET}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        print(score_board)
    
    def reset_game(self) -> None:
        """
        Reset the game with a new board and cleared out scores
        """
        self._board = self._create_board()
        self._ship_count = self.SHIPS
        

    def play_game(self, conn, send_fn, receive_fn) -> None:
        """
        Initiate gameplay. Client will always go first as a courtesy
        Utilizes the socket connection and it's send and receive functions to communicate
        """
        
        self._logo()
        
        # client initiation logic
        if self.turn == 1:
            while True:
                client_send = send_fn(conn)
                server_response = receive_fn(conn)
                if server_response.lower() == 'y' and client_send.lower() == 'y':
                    break
        
        # get confirmation from client and server to play
        elif self.turn == 2:
            while True:
                client_response = receive_fn(conn)
                server_send = send_fn(conn)
                
                if client_response.lower() == 'y' and server_send.lower() == 'y':
                    break


        # main game loop
        while not self._game_over():
            self.send_receive_score(conn, receive_fn)
            self._print_board()
            
            # send
            if self.turn == 1:
                # Player 1's turn 
                while True:
                    first_row = input("Row?")
                    first_col = input("Col?")
                    check, x, y = self._your_turn(first_row, int(first_col))
                    if check:
                        break
                # send your move
                send_fn(conn, f'{x},{y}')
                # wait for result of move
                received = receive_fn(conn)
                
                # self.send_receive_score(conn, receive_fn)
                # self._print_board()
                print(received)
                
                # now player 2's turn
                print("Waiting on opponent...")
                received = receive_fn(conn)
                x,y = tuple(received.split(','))
                result, message = self._opps_turn(x, y)
                
                # self.send_receive_score(conn, receive_fn)
                # self._print_board()
                print(message)

                # send result of move
                send_fn(conn, message)

            # receive 
            if self.turn == 2:
                # waiting for player 1
                print("Waiting on opponent...")
                received = receive_fn(conn)
                x,y = tuple(received.split(','))
                result, message = self._opps_turn(x, y)
                
                # self.send_receive_score(conn, receive_fn)
                # self._print_board()
                print(received)
                
                # send result of move
                send_fn(conn, message)
                # now player 2's turn
                while True:
                    first_row = input("Row?")
                    first_col = input("Col?")
                    check, x, y = self._your_turn(first_row, int(first_col))
                    if check:
                        break
                # send your move
                send_fn(conn, f'{x},{y}')
                # wait for result of move
                received = receive_fn(conn)

                # self.send_receive_score(conn, receive_fn)
                # self._print_board()
                print(received)


        
        # play again 
        self.play_game(conn, send_fn, receive_fn)
        return

        
        


# # range has to be 10 or less
# matrix_size = 10
# ships = 20

# board = [['.' for col in range(matrix_size)] for row in range(matrix_size)]

# # fill the board with 10 random stars
# positions = set()
# while len(positions) < ships:
#     coord = (random.randint(0, matrix_size-1), random.randint(0, matrix_size-1))
#     positions.add(coord)

# for x,y in positions:
#     board[x][y] = "o"


# top_labels = range(matrix_size)
# side_labels = string.ascii_uppercase[:matrix_size]
# print(side_labels)

# print(" ", *[*top_labels])
# for row in range(matrix_size):
#     print(side_labels[row], end=" ")
#     print(*board[row])

# KEYS = {letter:index for index, letter in enumerate(string.ascii_lowercase[:matrix_size])}
# print(KEYS)