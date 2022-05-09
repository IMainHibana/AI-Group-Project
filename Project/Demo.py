from cmath import exp
import itertools
from lib2to3.pgen2.driver import Driver
from turtle import pos
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
np.random.seed(14)
# import pyGame
import sys

INITIAL_STATE_M = np.array([4, 2])  # INITIAL STATE OF MALE AGENT
INITIAL_STATE_F = np.array([0, 2])  # INITAL STATE OF FEMALE AGENT
PICKUP = np.array([[2, 4], [3, 1]])  # LIST OF PICKUP STATES
DROP_OFF = np.array([[0, 0], [0, 4], [2, 2], [4, 4]])  # LIST OF DROP OFF STATES

class Game:
    def __init__(self):
        # 3D array board
        self.board = np.zeros([5, 5, 1])
        self.end_board = self.board.copy()

        # Hard coded pickup values into the board
        self.board[3, 1] = 10
        self.board[2, 4] = 10

        # Hard coded end_state board
        self.end_board[0, 0] = 5
        self.end_board[0, 4] = 5
        self.end_board[2, 2] = 5
        self.end_board[4, 4] = 5

        self.all_female_locs = np.array([0, 2])
        self.all_male_locs = np.array([4, 2])

        # All possible moves
        self.moves = ("up", "down", "left", "right", "pickup", "dropoff")

        # Agent location on map
        self.M_loc = INITIAL_STATE_M
        self.F_loc = INITIAL_STATE_F

    # List of possible action with their respective reward
    def action(self, agent, action):
        if (agent == "F"):
            temporary = self.F_loc
        elif (agent == "M"):
            temporary = self.M_loc

        if action == "up":
            temporary = np.array([temporary[0] - 1, temporary[1]])
            if (agent == "F"):
                self.F_loc = temporary
            elif (agent == "M"):
                self.M_loc = temporary
            return -1

        elif action == "down":
            temporary = np.array([temporary[0] + 1, temporary[1]])
            if (agent == "F"):
                self.F_loc = temporary
            elif (agent == "M"):
                self.M_loc = temporary
            return -1

        elif action == "left":
            temporary = np.array([temporary[0], temporary[1] - 1])
            if (agent == "F"):
                self.F_loc = temporary
            elif (agent == "M"):
                self.M_loc = temporary
            return -1

        elif action == "right":
            temporary = np.array([temporary[0], temporary[1] + 1])
            if (agent == "F"):
                self.F_loc = temporary
            elif (agent == "M"):
                self.M_loc = temporary
            return -1

        elif action == "pickup":
            if (agent == "F"):
                self.all_female_locs = np.append(self.all_female_locs, ["pickup", ])
            elif(agent == "M"):
                self.all_male_locs = np.append(self.all_male_locs, ["pickup", ])
            return 13

        elif action == "dropoff":
            if (agent == "F"):
                self.all_female_locs = np.append(self.all_female_locs, ["dropoff", ])
            elif (agent == "M"):
                self.all_male_locs = np.append(self.all_male_locs, ["dropoff", ])
            return 13

        else:
            print("====================no possible action=======================")
            exit

    # Check to see what possible moves are available to choose from
    def check_possible_action(self, agent, possible_directions):
        result_possible_directions = possible_directions.copy()
        if (agent == "F"):
            for direction in possible_directions:
                temporary_loc = self.F_loc.copy()
                if (direction == "up"):
                    temporary_loc[0] -= 1
                    if (np.array_equal(temporary_loc, self.M_loc) or 
                            temporary_loc[0] < 0 or temporary_loc[0] > 4):
                        result_possible_directions.remove("up")    
                elif (direction == "down"):
                    temporary_loc[0] += 1
                    if (np.array_equal(temporary_loc, self.M_loc) or 
                            temporary_loc[0] < 0 or temporary_loc[0] > 4):
                        result_possible_directions.remove("down")
                elif (direction == "left"):
                    temporary_loc[1] -= 1
                    if (np.array_equal(temporary_loc, self.M_loc) or 
                            (temporary_loc[1] < 0) or (temporary_loc[1] > 4)):
                        result_possible_directions.remove("left")
                elif (direction == "right"):
                    temporary_loc[1] += 1
                    if (np.array_equal(temporary_loc, self.M_loc) or 
                            temporary_loc[1] < 0 or temporary_loc[1] > 4):
                        result_possible_directions.remove("right")

        elif (agent == "M"):
            for direction in possible_directions:
                temporary_loc = self.M_loc.copy()
                if (direction == "up"):
                    temporary_loc[0] -= 1
                    if (np.array_equal(temporary_loc, self.F_loc) or (
                            temporary_loc[0] < 0 or temporary_loc[0] > 4)):
                        result_possible_directions.remove("up")
                elif (direction == "down"):
                    temporary_loc[0] += 1
                    if (np.array_equal(temporary_loc, self.F_loc) or (
                            temporary_loc[0] < 0 or temporary_loc[0] > 4)):
                        result_possible_directions.remove("down")
                elif (direction == "left"):
                    temporary_loc[1] -= 1
                    if (np.array_equal(temporary_loc, self.F_loc) or (
                            temporary_loc[1] < 0 or temporary_loc[1] > 4)):
                        result_possible_directions.remove("left")
                elif (direction == "right"):
                    temporary_loc[1] += 1
                    if (np.array_equal(temporary_loc, self.F_loc) or (
                            temporary_loc[1] < 0 or temporary_loc[1] > 4)):
                        result_possible_directions.remove("right")
            
        print(result_possible_directions)
        return result_possible_directions

    def q_values(self, state_size, action_size = 6):
        q_table = np.zeros((state_size, action_size))
        print(q_table)

    # Check to see if the game has reached final state
    def end_game(self):
        if (np.array_equal(self.board, self.end_board)):
            print("===============================Terminal State Reached=============")
            return True
        else:
            return False

    def render(self):
        print("Female location")
        print(self.F_loc)
        print("Male location")
        print(self.M_loc)
        self.all_female_locs = np.append(self.all_female_locs, self.F_loc)
        self.all_male_locs = np.append(self.all_male_locs, self.M_loc)
        #print("all female moves:")
        #print(self.all_female_locs)
        #print("all male moves:")
        #print(self.all_male_locs)
        #self.q_values()


class Agent:
    def __init__(self, alpha, gamma):
        # Initiate agent depending on the sex
        self.current_loc = np.array([-1, -1])
        self.carrying = False

    # Prandom function call
    def Prandom(self, game, agent):
        self.agent = agent
        if (agent == "F"):
            self.current_loc = game.F_loc
        elif (agent == "M"):
            self.current_loc = game.M_loc

        if ((np.array_equal(self.current_loc, PICKUP[0]) or np.array_equal(self.current_loc,
                                                                           PICKUP[1]))) and self.carrying is False:
            game.board[self.current_loc] -= 1
            self.carrying = True
            print("testingpickup")
            return "pickup"

        elif (np.array_equal(self.current_loc, DROP_OFF[0]) or np.array_equal(self.current_loc,
                                                                              DROP_OFF[1]) or np.array_equal(
                self.current_loc, DROP_OFF[2]) or np.array_equal(self.current_loc,
                                                                 DROP_OFF[3])) and self.carrying is True:
            game.board[self.current_loc] += 1
            self.carrying = False
            print("testingdrop")
            return "dropoff"

        else:
            possible_directions = ["up", "down", "left", "right"]
            choices = game.check_possible_action(agent, possible_directions)
            choice = np.random.choice(choices)
            return choice






