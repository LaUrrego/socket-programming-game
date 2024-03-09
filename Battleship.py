import random
import string
import os
from typing import List, Tuple
from Colors import ColorsBg, ColorsFg
import time

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
        if xpos == "/q" or ypos == "/q" or xpos == "/quit" or ypos == "/quit":
            return True, "/quit"
        
        xnum = self.KEYS[xpos.upper()]
        ynum = int(ypos)

        if self._board[xnum][ynum] == self.SHIP_PIECE:
            self._board[xnum][ynum] = "x" 
            self._ship_count -= 1
            print(f"    >{ColorsFg.red}You were hit!{self.RESET} Ship {xpos},{ypos} is down!")
            return True, f"    >{ColorsFg.green}You hit the opponent's ship{self.RESET}: {xpos},{ypos}!"
        self._board[xnum][ynum] = "x"
        print(f"    >{ColorsFg.lightblue}They missed!{self.RESET}")
        return False, f"    >{ColorsFg.lightblue}You missed!{self.RESET}"

        
    def _your_turn(self, xpos, ypos) -> Tuple[bool,str,str]:
        """
        Current player's turn
        """
        if xpos == "/q" or ypos == "/q" or xpos == "/quit" or ypos == "/quit":
            return True, "/quit", "/quit"
        
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
        message = f'\n#######################################\n{self.LOGO_COLOR}SHIP BATTLE{self.RESET}\nThe Un-Battleship!\nClient always goes first. To end the game and go back to chat, enter /q\nGuess where your opponents ship is by entering a row then column\nThe first to sink all their opponents ships wins!\n#######################################\n\nStarting soon, get ready!...\n'
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
        score = rec_fn(conn)
        if score == 'end':
            return True, False
        elif score == '/quit' or score =='/q':
            return True, True
        score = int(score)
        score_board = f'\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n| {self.PLAYER_COLOR}Player: {self.turn}{self.RESET}\n| Your Ships: {self.SCORE_YOUR_SHIPS}{self._ship_count}{self.RESET}\n| Opponent Ships: {self.SCORE_OPP_SHIPS}{score}{self.RESET}\n| Hit Count: {self.SCORE_YOUR_SHIPS}{self.SHIPS - score}{self.RESET}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
        print(score_board)
        return None, None
    
    def reset_game(self) -> None:
        """
        Reset the game with a new board and cleared out scores
        """
        self._board = self._create_board()
        self._ship_count = self.SHIPS
    
    def player_action(self):
        """
        Method to facilitate making a valid move
        """
        while True:
            row = input("\nRow? ")
            col = input("Col? ")
            check, x, y = self._your_turn(row, col)
            if check:
                return x,y
        

    def play_game(self, conn, send_fn, receive_fn) -> None:
        """
        Initiate gameplay. Client will always go first as a courtesy
        Utilizes the socket connection and it's send and receive functions to communicate
        """
        game_active = True
        
        while game_active:
            # prepared new game
            self.reset_game()
            self._logo()

            time.sleep(2)

            while not self._game_over():
                end_check, quit_check = self.send_receive_score(conn, receive_fn)
                if end_check:
                    if quit_check:
                        game_active = False
                    break
                self._print_board()

                if self.turn == 1:
                    # Player 1 actions
                    x, y = self.player_action()
                    print("\nWaiting on other player...\n")
                    if x == '/quit' or y == '/quit':
                        game_active = False
                        # notify connected player
                        receive_fn(conn)
                        send_fn(conn, '/quit')
                        break

                    send_fn(conn, f'{x},{y}')
                    received = receive_fn(conn)

                    # on-demand quit
                    if received == '/quit' or received == '/q':
                        game_active = False
                        break
                    elif received == 'end':
                        break
                    else:
                        x,y = tuple(received.split(','))
                        result, message = self._opps_turn(x, y)

                        send_fn(conn, message)
                        received = receive_fn(conn)
                        print(received)
                
                if self.turn == 2:
                    # player 2 actions
                    x, y = self.player_action()
                    print("\nWaiting on other player...\n")
                    if x == '/quit' or y == '/quit':
                        game_active = False
                        # notify connected player
                        receive_fn(conn)
                        send_fn(conn, '/quit')
                        break

                    send_fn(conn, f'{x},{y}')
                    received = receive_fn(conn)
                    
                    # on-demand quit
                    if received == '/quit' or received == '/q':
                        game_active = False
                        break
                    elif received == 'end':
                        break
                    else:
                        x,y = tuple(received.split(','))
                        result, message = self._opps_turn(x, y)

                        send_fn(conn, message)
                        received = receive_fn(conn)
                        print(received)
                
                print("Next round coming...")
                
                time.sleep(2)
                
            if game_active:

                if self._game_over():
                    # you lost
                    send_fn(conn, 'end')
                    print(f"{ColorsFg.yellow}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{self.RESET}")
                    print(f"\n{ColorsFg.red}Oh no, you lost!{self.RESET} Get them in the next one!\n")
                else:
                    # you won
                    print(f"{ColorsFg.yellow}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{self.RESET}")
                    print(f"\n{ColorsFg.green}You win!{self.RESET}\n")

                print(f"\n{ColorsFg.lightcyan}Game over! 3 seconds until restart...{self.RESET}\n")
                print(f"{ColorsFg.yellow}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{self.RESET}")

                time.sleep(3)


        print("Exiting to chat...")
        
        time.sleep(1)
            

        # self._logo()
        
        # client initiation logic
        # if self.turn == 1:
        #     while True:
        #         client_send = send_fn(conn)
        #         server_response = receive_fn(conn)
        #         if server_response.lower() == 'y' and client_send.lower() == 'y':
        #             break
        
        # # get confirmation from client and server to play
        # elif self.turn == 2:
        #     while True:
        #         client_response = receive_fn(conn)
        #         server_send = send_fn(conn)
                
        #         if client_response.lower() == 'y' and server_send.lower() == 'y':
        #             break


        # # main game loop
        # while not self._game_over():
        #     end_check = self.send_receive_score(conn, receive_fn)
        #     if end_check: break
        #     self._print_board()
            
        #     # send
        #     if self.turn == 1:
        #         # Player 1's turn 
        #         while True:
        #             first_row = input("Row?")
        #             first_col = input("Col?")
        #             check, x, y = self._your_turn(first_row, int(first_col))
        #             if check:
        #                 break
                # send your move
                # send_fn(conn, f'{x},{y}')
                # # wait for result of move
                # received = receive_fn(conn)
                
                # # self.send_receive_score(conn, receive_fn)
                # # self._print_board()
                # print(received)
                
                # # now player 2's turn
                # print("Waiting on opponent...")
                # received = receive_fn(conn)
                # x,y = tuple(received.split(','))
                # result, message = self._opps_turn(x, y)
                
                # # self.send_receive_score(conn, receive_fn)
                # # self._print_board()
                # print(message)

            #     # send result of move
            #     send_fn(conn, message)

            # # receive 
            # if self.turn == 2:
            #     # waiting for player 1
            #     print("Waiting on opponent...")
            #     received = receive_fn(conn)

            #     x,y = tuple(received.split(','))
            #     result, message = self._opps_turn(x, y)
                
            #     # self.send_receive_score(conn, receive_fn)
            #     # self._print_board()
            #     print(received)
                
            #     # send result of move
            #     send_fn(conn, message)
            #     # now player 2's turn
                # while True:
                #     first_row = input("Row?")
                #     first_col = input("Col?")
                #     check, x, y = self._your_turn(first_row, int(first_col))
                #     if check:
                #         break
                # # send your move
                # send_fn(conn, f'{x},{y}')
                # # wait for result of move
                # received = receive_fn(conn)

                # # self.send_receive_score(conn, receive_fn)
                # # self._print_board()
                # print(received)

        # # exiting while-loop
        # if self._game_over():
        #     # you lost
        #     print("Oh no, you lost! Get them in the next one!")
        #     print("Game will reset in 5 seconds!")
        #     send_fn(conn, "end")
        # else:
        #     # you won
        #     print("You win!")
        #     print("Game will reset in 5 seconds!")

        # # do a timeout to wait
        # time.sleep(5)
            
        # # reset 
        # self.reset_game()
            

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