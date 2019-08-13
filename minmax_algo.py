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



# ([1, 2, 3, 4, 5, 7], "cpu") would return {6:0, 8:0, 9:10}
def check_level_up(game_t, player, check_op=False):
    # return scores at game t+1 for each possible move
    brd = copy_board(game_t, player)
    available_moves = np.setdiff1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), game_t)
    var = {move:0 for move in available_moves}
    for move in available_moves:
        board_t =  deepcopy(brd)
        if player == "cpu":
            if check_op == False:
                board_t.write_move(move, 'O')
                status = board_t.check_for_victory()
                if status != False:
                    var[move] = 10
            else:
                board_t.write_move(move, 'X')
                status = board_t.check_for_victory()
                if status != False:
                    var[move] = -10

        else:
            if check_op == False:
                board_t.write_move(move, 'X')
                status = board_t.check_for_victory()
                if status != False:
                    var[move] = -10
            else:
                board_t.write_move(move, 'O')
                status = board_t.check_for_victory()
                if status != False:
                    var[move] = 10
    return var



def recursion(game_t0, origin=True, var=None, move_checked=None, len_start=None):
    # use the len of the game before starting the recursion to keep track of depth
    if len_start == None:
        len_start = len(game_t0)
    # compute depth, depth == 0 before recursion
    depth = len(game_t0) - len_start
    # available moves for this specific recursion
    available_moves_t0 = np.setdiff1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), game_t0)

    # define the value of each possible move before starting any recursivity
    if depth == 0:
        var = check_level_up(game_t0, "cpu")
        if min(check_level_up(game_t0, "cpu", check_op=True).values()) == -10:
            value_human_wining = min(check_level_up(game_t0, "cpu", check_op=True), key=check_level_up(game_t0, "cpu", check_op=True).get)
            losing_moves = np.setdiff1d(available_moves_t0, value_human_wining)
            for i in losing_moves:
                var[i] = -10
            return var

    # create a temporary evaluation of possible moves outcome
    # temporary because could be the recursive move, not the one under evaluation
    if depth % 2 == 0: # cpu turn:
        var_temp0 = check_level_up(game_t0, "cpu")
    else: # human turn
        var_temp0 = check_level_up(game_t0, "human")

    # only during recursion
    if depth > 0:
        # write the value of the originally evalutated move that brings
        # an outcome (win or loose)
        # make sure it doesnt overwrite var if already a value in it form a less deeper recursion
        if depth % 2 == 0: # cpu turn:
            if max(var_temp0.values()) == 10 and var[move_checked] == 0:
                var[move_checked] = 10
        else: # human turn
            if min(var_temp0.values()) == -10 and var[move_checked] == 0:
                var[move_checked] = -10
            elif var[move_checked] == 0 and max(check_level_up(game_t0, "human", check_op=True).values()) == 10:
                # if a move makes the human win, this move will be 0, all other set at -10
                if any(i == 0 for i in var_temp0.values()):
                    value_cpu_wining = max(check_level_up(game_t0, "human", check_op=True), key=check_level_up(game_t0, "cpu").get)
                    available_moves_t0 = np.setdiff1d(available_moves_t0, value_cpu_wining)

    # run only if more than one move left
    if len(available_moves_t0) != 1:
        for move in available_moves_t0:
            # run only if there is no outcome yet for this move
            if var_temp0[move] == 0:
                game_t1 = game_t0 + [move]
                # Before starting the recursion, keep track of the move under evaluation
                if  move_checked==None:
                    move_checked = move
                    turn = 0
                recursion(game_t1, origin=True, var=var, move_checked=move_checked, len_start=len_start)
                # check if under recursivity, if not, update the move under evaluation
                if origin == True:
                    move_checked = move
    return var


class board_proba:
    """
    This class create the board structure, print it, update it,
    check for winning position, highlight winning position, check if board full or still move available
    """
    def __init__(self):
        self.board = ['    '] * 10

    def print_board(self):
        position = self.board
        print(' ' + position[1] + ' | ' + position[2] + ' | ' + position[3])
        print('-----------------')
        print(' ' + position[4] + ' | ' + position[5] + ' | ' + position[6])
        print('-----------------')
        print(' ' + position[7] + ' | ' + position[8] + ' | ' + position[9])

    def write_probas(self, position, proba):
        # Write move on board
        self.board[position] = proba

def print_probas(probas):
    brd = board_proba()
    for ind, proba in enumerate(probas):
        if proba == 999:
            brd.write_probas(ind+1, "   ")
        else:
            proba_ = proba
            brd.write_probas(ind+1, proba_)
    return brd.print_board()

def minmax_cpu(current_game, verbose=False):
    var = recursion(current_game)
    if verbose == True:
        probas = [999] * 9
        for i in var.keys():
            if var[i] == 0:
                probas[i-1] = " {} ".format(var[i])
            elif var[i] == 10:
                probas[i-1] = " {}".format(var[i])
            else:
                probas[i-1] = "{}".format(var[i])
        print(" ")
        print("\x1b[10;10;31m*** CHECKING PROBA ****\x1b[0m")
        print("likely to win:")
        print_probas(probas)
        print(" ")
    return max(var, key=var.get)





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
        comb_dict = {}
        for combination in self.list_combinations:
            comb_tuple= ()
            brd = deepcopy(self.brd)
            print("checking comb {}".format(combination))
            stop = False
            for ind, move in enumerate(combination):
                print("checking move {}".format(move))
                player = "O" if ind%2 == 0 else "X"
                comb_tuple = comb_tuple + (move,)
                print(comb_tuple)
                brd.write_move(move, player)
                victory = brd.check_for_victory()
                print("victory = {}".format(victory))
                if victory != False and stop == False:
                    comb_dict[comb_tuple] = 10 if victory == "O" else -10
                    stop = True
        return comb_dict

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

def evaluate_move(current_game, move):
    outputs = combinations(current_game).compute_output()
    keys = preprocess_keys(outputs)
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
