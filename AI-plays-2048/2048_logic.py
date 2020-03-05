import numpy as np
import random
from itertools import product
import math
def initialize_game(size):
    board = np.zeros((size*size))
    initial_twos =  np.random.default_rng().choice(16, 2, replace=False)
    board[initial_twos] = 2
    board = board.reshape((size, size))

    return board

class Board:
    def __init__(self, size):
        self.board = initialize_game(size)
        self.size = size
        self.WIN_VALUE = 2048
        self.NEW_TILE_DISTRIBUTION = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
        self.SEARCH_LENGTH = 5
        self.NUMBER_OF_SEARCHES = 100
        self.DIRECTIONS = ["DOWN", "UP", "LEFT", "RIGHT"]
        self.NON_VALID_MOVES = 10

    def check_for_win(self):
        is_win = False
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == self.WIN_VALUE:
                    is_win = True
        return is_win
       
    def check_for_move(self):
        has_move = False
        for row, col in product(range(self.size), range(self.size)):
            if self.board[row][col] == 0:
                has_move = True
                break
            try:
                if self.board[row][col] == self.board[row+1][col] or self.board[row][col+1] == self.board[row][col]:
                    has_move = True
                    break
            except IndexError:
                pass
        return has_move

    def push_row_right(self, a_row):
        a_row = np.concatenate((a_row[a_row==0], a_row[a_row!=0]))
        return a_row
    
    def push_board_right(self):
        initial_board = np.copy(self.board)
        self.board = np.apply_along_axis(self.push_row_right, 1, self.board)

    def merge_elements(self):
        for col in range(self.size-1, 0, -1):
            same_to_left_mask = np.equal(self.board[:, col], self.board[:, col-1])
            self.board[:, col] = np.multiply(1+same_to_left_mask, self.board[:,col])
            self.board[:, col-1] = np.multiply(np.logical_not(same_to_left_mask), self.board[:,col-1])

    def make_move(self, direction):
        prev_board = np.copy(self.board)
        if direction == "DOWN":
            self.board = np.rot90(self.board)
            self.push_board_right()
            self.merge_elements()
            self.push_board_right()
            self.board = np.rot90(self.board, 3)
        elif direction == "UP":
            self.board = np.rot90(self.board, 3)
            self.push_board_right()
            self.merge_elements()
            self.push_board_right()
            self.board = np.rot90(self.board)

        elif direction == "LEFT":
            self.board = np.rot90(self.board, 2)
            self.push_board_right()
            self.merge_elements()
            self.push_board_right()
            self.board = np.rot90(self.board, 2)

        elif direction == "RIGHT":
            self.push_board_right()
            self.merge_elements()
            self.push_board_right()
        else:
            pass

        if not np.array_equal(prev_board, self.board):
            tile_value = self.NEW_TILE_DISTRIBUTION[random.randint(0, len(self.NEW_TILE_DISTRIBUTION)-1)]
            tile_row_options, tile_col_options = np.nonzero(np.logical_not(self.board))
            # print("Number of tile row options is ", (len(tile_row_options)-1))
            tile_location = random.randint(0, len(tile_row_options)-1)
            self.board[tile_row_options[tile_location], tile_col_options[tile_location]] = tile_value
            move_was_made = True
        else:
            move_was_made = False
        return move_was_made

    def board_evaluation(self):
        if self.WIN_VALUE in self.board:
            return self.WIN_VALUE
        else:
            return np.mean(self.board)
    
    def move_maker(self):
        actual_board = np.copy(self.board)
        move_results = np.zeros(4)
        for first_move in range(4):
            for _ in range(self.NUMBER_OF_SEARCHES):
                self.make_move(self.DIRECTIONS[first_move])
                non_valid_moves = 0
                step = 0
                while step < self.SEARCH_LENGTH:
                    direction = self.DIRECTIONS[random.randint(0, 3)]
                    move_was_made = self.make_move(direction)
                    if move_was_made:
                        step += 1
                    else: 
                        non_valid_moves += 1
                    if non_valid_moves == self.NON_VALID_MOVES:
                        break
                evaluation = self.board_evaluation()
                move_results[first_move] += evaluation
                self.board = actual_board
        move = move_results.argmax()
        print(self.DIRECTIONS[move])
        self.make_move(self.DIRECTIONS[move])
    
    def test_ai(self):
        for i in range(1000):
            print(self.board)
            print(i)
            self.move_maker()
        print(self.board)

board = Board(4)
board.test_ai()
