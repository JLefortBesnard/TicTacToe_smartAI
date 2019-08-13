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
import itertools
import pandas as pd


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





def copy_board(game_t, first_player):
    brd = board()
    if first_player == "cpu":
        starter = 'O' if len(game_t) % 2 == 0 else 'X'
        opponent = 'O' if starter == 'X' else 'X'
    else:
        starter = 'X' if len(game_t) % 2 == 0 else 'O'
        opponent = 'X' if starter == 'O' else 'O'
    # reconfigure the board as in game_t
    for ind, move in enumerate(game_t):
        symbole = starter if ind % 2 == 0 else opponent
        brd.write_move(move, symbole)
    return brd




import itertools
class combinations:
    def __init__(self, current_game):
        first_player = "cpu" if len(current_game)%2 == 0 else "human"
        self.available_moves = np.setdiff1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), current_game)
        self.value = {i:0 for i in self.available_moves}
        self.brd = copy_board(current_game, first_player)
        self.list_combinations = list(itertools.permutations(self.available_moves))
        self.current_game = current_game

    def check_script(self):
        print(self.available_moves, self.value, self.list_combinations)
        self.brd.print_board()

    def compute_output(self):
        df = pd.DataFrame(999, columns = [1,2,3,4,5,6,7,8,9,"output"], index=[i for i in range(len(self.list_combinations))])
        comb_dict = {}
        for t, combination in enumerate(self.list_combinations):
            comb_tuple= ()
            brd = deepcopy(self.brd)
            end = len(combination)
            stop = False
            turn = 1
            for ind, move in enumerate(combination):
                print("iterate= {} over {}".format(move, combination))
                player = "O" if ind%2 == 0 else "X"
                comb_tuple = comb_tuple + (move,)
                if stop == False:
                    df[ind+1].iloc[t] = move
                brd.write_move(move, player)
                victory = brd.check_for_victory()
                if victory != False and stop == False:
                    point = 10 if victory == "O" else -10
                    comb_dict[comb_tuple] = point
                    df["output"].iloc[t] = point
                    stop = True
                elif turn == end and stop == False:
                    comb_dict[comb_tuple] = 0
                    df["output"].iloc[t] = 0
                turn += 1
        df.drop_duplicates(inplace=True)
        return comb_dict, df

    def return_values(self):
        for move in self.available_moves:
            status = evaluate_move(self.current_game, move)
            self.value[move] = status
        return self.value


def preprocess_keys(outputs):
    keys = [()] * 9
    for key in outputs.keys():
        pos = len(key)-1
        keys[pos] = keys[pos] + key
    for ind, key in enumerate(keys):
        nb_shunk = len(key)/(ind+1)
        if nb_shunk > 1:
            keys[ind] = np.split(np.array(keys[ind]), nb_shunk)
            for i, split in enumerate(keys[ind]):
                keys[ind][i] = tuple(split)
            keys[ind] = tuple(keys[ind])
    return keys
"""
def evaluate_move(current_game, move):
    outputs = combinations(current_game).compute_output()[0]
    keys = preprocess_keys(outputs)
    keys_dynamic = deepcopy(keys)
    for ind, shunk in enumerate(keys):
        switch = 0 if ind % 2 ==0 else 1
        if switch == 0:
            if len(shunk) > 1:
                for sh in shunk:
                    if outputs[sh] == 10 and sh[0] == move:
                        return 10
            elif len(shunk) == 1:
                    if outputs[shunk] == 10 and shunk[0] == move:
                        return 10
        else:
            if len(shunk) > 1:
                for sh in shunk:
                    if outputs[sh] == -10 and sh[0] == move:
                        return -10
            elif len(shunk) == 1:
                    if outputs[shunk] == -10 and shunk[0] == move:
                        return -10
    return 0
"""


# same but with dataframe
def evaluate_move(current_game, move):
    outputs = combinations(current_game).compute_output()[1]
    stop = False
    df = outputs
    df_move = df[df[1]==move]
    max_iter = 9 - len(current_game)
    for i in range(max_iter):
        switch = 0 if i % 2 ==0 else 1
        if switch == 0: # cpu move
            if any(df_move["output"][df_move[i+2]==999]==10):
                return 10
        else:
            if any(df_move["output"][df_move[i+2]==999]==-10):
                return -10
            # remove possibility of opponent to win if possible
            possible_moves = []
            for possible_move in df_move[i+1]:
                if possible_move != 999:
                    possible_moves.append(possible_move)
            possible_moves = list(set(possible_moves))
            for move in possible_moves:
                done = False
                if all(df_move["output"][df_move[i+1] == move] == 0):
                    df_move = df_move[df_move[i+1] == move]
                    done = True
    return 0



def pruning_cpu(current_game):
    available_moves = np.setdiff1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), current_game)
    values = {i:0 for i in available_moves}
    for move in available_moves:
        values[move] = evaluate_move(current_game, move)
    return max(values, key=values.get)
