"""
Tictactoe game
human vs hand-crafted AI (no training involved)
2019
Author:
        Jeremy Lefort-Besnard   jlefortbesnard (at) tuta (dot) io
"""

#Library we need
from sys import platform as sp
import numpy as np
from os import system
from copy import deepcopy

class board:
    """
    This class create the board structure, print it, update it,
    check for winning position, highlight winning position, check if board full or still move available
    """
    def __init__(self):
        self.board = [' '] * 10

    def print_board(self):
        position = self.board
        print(' ' + position[1] + ' | ' + position[2] + ' | ' + position[3])
        print('-----------')
        print(' ' + position[4] + ' | ' + position[5] + ' | ' + position[6])
        print('-----------')
        print(' ' + position[7] + ' | ' + position[8] + ' | ' + position[9])

    def write_move(self, move, symbole):
        # Write move on board
        self.board[move] = symbole

    def check_for_victory(self):
        victory = False
        # winning combinations
        victory_combinations = [[1,2,3], [4,5,6], [7,8,9], [1,5,9], [7,5,3], [1,4,7], [2,5,8], [3,6,9]]
        for combination in victory_combinations:
            pos1, pos2, pos3 = combination[0], combination[1], combination[2]
            if self.board[pos1] == self.board[pos2] == self.board[pos3] != " ":
                # return the symbole (O or X) that won the game
                victory = self.board[pos1]
        return victory



# AI
def procedural_cpu(current_game):
    # reccreate the board of the ongoing game:
    starter = 'O' if len(current_game) % 2 == 0 else 'X' # define if cpu or human was the starter
    opponent = 'O' if starter == 'X' else 'X'
    brd = board()
    for ind, move in enumerate(current_game):
        symbole = starter if ind % 2 == 0 else opponent
        brd.write_move(move, symbole)
    # diplay possible moves
    available_moves = np.setdiff1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), current_game)
    best_move = 0
    for move in available_moves:
        vitual_check_win = deepcopy(brd)
        vitual_check_win.write_move(move, 'O')
        vitual_check_loose = deepcopy(brd)
        vitual_check_loose.write_move(move, 'X')
        # Check if a move can be a winning move, return it if so
        if vitual_check_win.check_for_victory() == 'O':
            return move
        # Check if a move from the opponent can make the AI loose, return it if so, to block the opponent
        if vitual_check_loose.check_for_victory() == 'X':
            # Not a return because winning is a priority over blocking (if no winning move, then block)
            best_move = move
    if best_move != 0:
        return best_move # return the move that block the opponent only if no winning move

    if 5 in available_moves:
            return 5 # best move to play if no winning or blocking move
    corners = [1, 3, 7, 9]
    for corner in corners:
        if corner in available_moves:
                return corner # best move to play if 5 not available and no winning or blocking move
    edges = [2, 4, 6, 8]
    for edge in edges:
        if edge in available_moves:
                return edge # best move to play if 5 not available and no winning or blocking move and no more empty corner
