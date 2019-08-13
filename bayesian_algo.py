import random
import os
import numpy as np
import pandas as pd
from random import choice
import platform
import time
from os import system


def load_data():
    path = "memory\\memory.xls"
    if not os.path.exists(path):
        data = pd.DataFrame(columns = ["move1", "move2", "move3","move4","move5","move6","move7","move8","move9", "output"])
    else:
        data = pd.read_excel(path)
    data["output"][data["output"] == -1] = 0
    return data

def index_similar_moves(current_game, memory):
    length_to_check = len(current_game)
    similar_moves = memory.iloc[:, :length_to_check].values == current_game
    index = []
    for ind, comparison in enumerate(similar_moves):
        if comparison.all() == True:
            index.append(ind)
    data_for_proba = memory.iloc[index]
    return data_for_proba

def bayes_posterior_winning_proba(data_for_proba, memory):
    output_current_game = data_for_proba["output"]
    all_outputs = memory["output"]
    try:
        pxo = len(data_for_proba[output_current_game == 1]) / len(memory[all_outputs == 1])
    except:
        return 2
    po = len(memory[all_outputs == 1]) / len(memory)
    px = len(data_for_proba) / len(memory)
    try:
        pox = (pxo * po)/px
        return pox
    except:
        return 2

def bayes_posterior_even_proba(data_for_proba, memory):
    output_current_game = data_for_proba["output"]
    all_outputs = memory["output"]
    try:
        pxo = len(data_for_proba[output_current_game == 0]) / len(memory[all_outputs == 0])
    except:
        return 2
    po = len(memory[all_outputs == 0]) / len(memory)
    px = len(data_for_proba) / len(memory)
    try:
        pox = (pxo * po)/px
        return pox
    except:
        return 2


def bayes_posterior_loosing_proba(data_for_proba, memory):
    output_current_game = data_for_proba["output"]
    all_outputs = memory["output"]
    try:
        pxo = len(data_for_proba[output_current_game == -1]) / len(memory[all_outputs == -1])
    except:
        return 2
    po = len(memory[all_outputs == -1]) / len(memory)
    px = len(data_for_proba) / len(memory)
    try:
        pox = (pxo * po)/px
        return pox
    except:
        return 2




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
        print('-------------------')
        print(' ' + position[4] + ' | ' + position[5] + ' | ' + position[6])
        print('-------------------')
        print(' ' + position[7] + ' | ' + position[8] + ' | ' + position[9])

    def write_probas(self, position, proba):
        # Write move on board
        self.board[position] = proba

def print_probas(probas):
    brd = board_proba()
    for ind, proba in enumerate(probas):
        if proba == 999:
            brd.write_probas(ind+1, "    ")
        elif proba == 2:
            brd.write_probas(ind+1, "    ")
        else:
            proba_ = str(np.round_(proba, decimals=2))
            brd.write_probas(ind+1, proba_)
    return brd.print_board()


def bayesian_cpu(current_game, verbose=False):
    available_moves = np.setdiff1d(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]), current_game)
    proba = 0
    best_move = 10
    memory = load_data()
    probas = [999] * 9
    for move in available_moves:
        game_to_check = current_game + [move]
        data_for_proba = index_similar_moves(game_to_check, memory)
        if len(current_game) % 2 == 0:
            data_for_proba = data_for_proba[data_for_proba["starter"] == 0]
        else:
            data_for_proba = data_for_proba[data_for_proba["starter"] == 1]
        proba_ = bayes_posterior_winning_proba(data_for_proba, memory)
        probas[move-1] = proba_
        if proba_*10 > proba*10 and proba_ != 2:
            proba = proba_
            best_move = move
    if verbose == True:
        print(" ")
        print("\x1b[10;10;31m*** CHECKING PROBA ****\x1b[0m")
        print("likely to win:")
        print_probas(probas)
        print(" ")
    if best_move != 10 and proba*10 != 0:
        print("best proba = {}".format(proba))
        print("***********************")
        return best_move
    else:
        proba = 0
        even_move = 10
        probas = [999] * 9
        for move in available_moves:
            game_to_check = current_game + [move]
            data_for_proba = index_similar_moves(game_to_check, memory)
            if len(current_game) % 2 == 0:
                data_for_proba = data_for_proba[data_for_proba["starter"] == 0]
            else:
                data_for_proba = data_for_proba[data_for_proba["starter"] == 1]
            proba_ = bayes_posterior_even_proba(data_for_proba, memory)
            probas[move-1] = proba_
            if proba_*10 > proba*10 and proba_ != 2:
                proba = proba_
                even_move = move
        print(" ")
        print("\x1b[10;10;31m*** CHECKING PROBA ****\x1b[0m")
        print("likely to even:")
        print_probas(probas)
        print(" ")
        if even_move != 10 and proba*10 != 0:
            print("best proba = {}".format(proba))
            print("***********************")
            return even_move
        else:
            worst_move = 10
            bad_choices = []
            probas = [999] * 9
            for move in available_moves:
                game_to_check = current_game + [move]
                data_for_proba = index_similar_moves(game_to_check, memory)
                if len(current_game) % 2 == 0:
                    data_for_proba = data_for_proba[data_for_proba["starter"] == 0]
                else:
                    data_for_proba = data_for_proba[data_for_proba["starter"] == 1]
                proba_ = bayes_posterior_loosing_proba(data_for_proba, memory)
                probas[move-1] = proba_
                if proba_ != 2:
                    bad_choices.append(move)
            choice = np.setdiff1d(available_moves, bad_choices)
            print(" ")
            print("likely to loose:")
            print_probas(probas)
            print(" ")
            try:
                print("random among = {}".format(choice))
                print("***********************")
                return np.random.choice(choice)
            except:
                print("random among available = {}".format(available_moves))
                print("***********************")
                return np.random.choice(available_moves)
