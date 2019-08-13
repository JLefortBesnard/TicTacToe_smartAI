"""
TicTacToe game with multiple choice of opponent (random, procedural, Bayesian, minmax algorithm)
2019
Author:
        Jeremy Lefort-Besnard   jlefortbesnard (at) tuta (dot) io
"""

#Library we need
from sys import platform as sp
import time
import os
import subprocess
import pandas as pd
import numpy as np

import platform
import time
from os import system
from random_algo import random_cpu
from bayesian_algo import bayesian_cpu
from procedural_algo import procedural_cpu
from minmax_algo import minmax_cpu
from pruning_algo import pruning_cpu



# create the board, update it
class board:
    """
    This class create the board structure, print it, update it at each move,
    look at the position of X and O to check for game status (victory/even)
    """
    # creates an empty board
    def __init__(self):
        self.board = [' '] * 10

    # displays the board on the terminal
    def print_board(self):
        position = self.board
        print(' ' + position[1] + ' | ' + position[2] + ' | ' + position[3])
        print('-----------')
        print(' ' + position[4] + ' | ' + position[5] + ' | ' + position[6])
        print('-----------')
        print(' ' + position[7] + ' | ' + position[8] + ' | ' + position[9])

    # writes the move on the board
    def move(self, move, symbole):
        self.board[move] = symbole

    # check if a move is allowed (for human player)
    def check_pos(self, move):
        if self.board[move] != ' ':
            return 1
        elif move not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            print("Forbidden move")
            return 1

    # check if the status of an ongoing game is a victory (3 same symboles aligned)
    def victory(self):
        victory = False
        # winning combinations
        victory_combinations = [[1,2,3], [4,5,6], [7,8,9], [1,5,9], [7,5,3], [1,4,7], [2,5,8], [3,6,9]]
        for combination in victory_combinations:
            pos1, pos2, pos3 = combination[0], combination[1], combination[2]
            if self.board[pos1] == self.board[pos2] == self.board[pos3] != " ":
                # return the symbole (O or X) that won the game
                victory = self.board[pos1]
        return victory


# Display the coordinate system used in this game, make it easier for the human player to know what to play
def position():
    print(' 1 | 2 | 3 ')
    print('-----------')
    print(' 4 | 5 | 6 ')
    print('-----------')
    print(' 7 | 8 | 9 ')

# clear the screen of your terminal in Linux, Mac or Windows
def clear_screen():
    if sp == "win32":
        os.system('cls')
    else:
        os.system('clear')

def cpu_thinks(cpu_type, current_game):
    if cpu_type == "r": #
        AI = random_cpu(current_game)
    elif cpu_type == "b":
        AI = bayesian_cpu(current_game)
    elif cpu_type == "m":
        AI = minmax_cpu(current_game)
    elif cpu_type == "p": #
        AI = pruning_cpu(current_game)
    else:
        AI = procedural_cpu(current_game)
    return AI

# Define who starts
def define_role():
    starter = input("Who starts, cpu (c) or human (h) ? >> ")
    return starter

# the human is the first player
def human_first(cpu_type):
    # create an empty board
    game = board()
    # necessary variable to set the end of the game in case of even
    nb_moves = 0
    # remember all the moves played during a game
    current_game = []
    # keep playing while no victory and less than 9 moves (full board=even)
    while game.victory() == False and nb_moves < 9:
        # ask the human player which move to make
        move = int(input(">> what move? >> "))
        # check that the human choice is possible
        while game.check_pos(move) == 1:
            print("move already chosen, pick an empty place (1 to 9):")
            move = int(input(">> what move? >> "))
        game.move(move, "X") # write the human move
        current_game.append(move) # memorize the move
        nb_moves += 1 # next turn
        game.print_board() # display the board on the terminal
        print("Turn {} ".format(nb_moves))
        time.sleep(1)

        # run if no victory and still possible move available
        if game.victory() == False and nb_moves < 9:
            cpu_choice = cpu_thinks(cpu_type, current_game)
            print("CPU plays {}".format(cpu_choice))
            game.move(cpu_choice, "O") # write the human move
            current_game.append(cpu_choice) # memorize the move
            nb_moves += 1 # next turn
            game.print_board()  # display the board on the terminal
            time.sleep(1)
    # return the current game history once the while loop is over because
    # there must be even or a victory for one of the 2 players
    # the status of the game will be check though the check_output function
    return game, current_game


# the CPU is the first player
def cpu_first(cpu_type):
    # create an empty board
    game = board()
    # necessary variable to set the end of the game in case of even
    nb_moves = 0
    # remember all the moves played during a game
    current_game = []
    # keep playing while no victory and less than 9 moves (full board=even)
    while game.victory() == False and nb_moves < 9:
        cpu_choice = cpu_thinks(cpu_type, current_game)
        print("CPU plays {}".format(cpu_choice))
        game.move(cpu_choice, "O") # write the human move
        current_game.append(cpu_choice) # memorize the move
        nb_moves += 1 # next turn
        game.print_board()  # display the board on the terminal
        time.sleep(1)

        # run if no victory and still possible move available
        if game.victory() == False and nb_moves < 9:
            # ask the human player which move to make
            move = int(input(">> what move? >> "))
            # check that the human choice is possible
            while game.check_pos(move) == 1:
                print("move already chosen, pick an empty place (1 to 9):")
                move = int(input(">> what move? >> "))
            game.move(move, "X") # write the human move
            current_game.append(move) # memorize the move
            nb_moves += 1 # next turn
            game.print_board() # display the board on the terminal
            print("Turn {} ".format(nb_moves))
            time.sleep(1)
    # return the current game history once the while loop is over because
    # there must be even or a victory for one of the 2 players
    # the status of the game will be check though the check_output function
    return game, current_game




def check_and_save_output(game, current_game, starter):
    # 3 possible scenarios once the while loop is over: even, win or loose
    if game.victory() == False:
        print("...........")
        print("Boring game")
        print("...........")
        output = np.array([current_game, 0]) # save the game for the cpu memory

    elif game.victory() != True:
        if game.victory() == "X":
            print("****************")
            print("victory for human! ({})".format(game.victory()))
            print("****************")
            output = np.array([current_game, -1]) # save the game for the cpu memory
        else:
            print("****************")
            print("victory for cpu! ({})".format(game.victory()))
            print("****************")
            output = np.array([current_game, 1]) # save the game for the cpu memory

    # save the game in an existing Dataframe (or create the dataframe) for the cpu memory
    path = "memory\\memory.xls"
    if not os.path.exists(path):
        df = pd.DataFrame(columns = ["move1", "move2", "move3","move4","move5","move6","move7","move8","move9", "output", "starter"])
    else:
        df = pd.read_excel(path)
    game_history = np.full(11, np.nan)
    for nb, i in enumerate(output[0]):
        game_history[nb] = i
    game_history[9] = output[1]
    game_history[10] = 0 if starter == "c" else 1
    # save the list output in a pandas dataframe
    row_number = len(df)
    df.loc[row_number] = game_history
    print("saving and quit...")
    # save the pandas dataframe output in an exel document
    df.to_excel(path, index=False)



# Processus of a complete game
def game():
    clear_screen()
    again = "y"
    print("which cpu do you want to compete with?")
    print("random: very easy (r)")
    print("Bayesian: becomes as smart as you as you play (b)")
    print("Minmax: impossible to beat and computationnaly expensive (m)")
    print("Pruning algorithm: computationnaly expensive and impossible to beat (p)")
    print("Procedural: impossible to beat (pro)")
    cpu_type = input("> ")
    while again == "y":
        print("You can choose among these positions: (remember them)")
        position() # display coordinate system of the game to make it easier for the player
        starter = define_role() # ask the human who starts
        output_game = human_first(cpu_type) if starter == "h" else cpu_first(cpu_type)
        check_and_save_output(output_game[0], output_game[1], starter)
        print(" " * 10 )
        again = input("play again? (y or n) > ")
        clear_screen()

# launch the game
game()
