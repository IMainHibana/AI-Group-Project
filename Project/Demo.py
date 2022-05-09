from cmath import exp
import itertools
from turtle import pos
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
#import pyGame
import sys

INITIAL_STATE_M = np.array([4, 2]) #INITIAL STATE OF MALE AGENT
INITIAL_STATE_F = np.array([0, 2]) #INITAL STATE OF FEMALE AGENT
PICKUP= np.array([[3, 5], [4, 2]]) #LIST OF PICKUP STATES
DROP_OFF = np.array([[1, 1], [1, 5], [3, 3], [5, 5]]) #LIST OF DROP OFF STATES

class Game:
    def __init__(self):
        #3D array board
        self.board = np.zeros([5,5,1])
        self.end_board = self.board.copy()

        #Hard coded pickup values into the board
        self.board[3, 1] = 10
        self.board[2, 4] = 10

        #Hard coded end_state board
        self.end_board[0,0] = 5
        self.end_board[0,4] = 5
        self.end_board[2,2] = 5
        self.end_board[4,4] = 5
        
        #All possible moves
        self.moves = ("up", "down", "left", "right", "pickup", "dropoff")

        #Agent location on map
        self.M_loc = INITIAL_STATE_M
        self.F_loc = INITIAL_STATE_F

    #List of possible action with their respective reward
    def action(self, action, agent):
        if action == "up":
            temporary = (temporary[0] - 1, temporary[1])
            return -1

        elif action == "down":
            temporary = (temporary[0] + 1, temporary[1])
            return -1

        elif action == "left":
            temporary = (temporary[0], temporary[1] - 1)
            return -1

        elif action == "right":
            temporary = (temporary[0], temporary[1] + 1)
            return -1
        
        elif action == "pickup":
            return 13
        
        elif action == "dropoff":
            return 13
        
        else:
            print("====================no possible action=======================")
            exit
    
    #Check to see what possible moves are available to choose from
    def check_possible_action(self, agent, possible_directions):
        if (agent == "F"):
            for direction in possible_directions:
                if(direction == "up"):
                    temporary_loc = self.F_loc
                    temporary_loc[0] += 1
                    if(temporary_loc == self.M_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "up"
                elif(direction == "down"):
                    temporary_loc = self.F_loc
                    temporary_loc[0] -= 1
                    if(temporary_loc == self.M_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "down"
                elif(direction == "left"):
                    temporary_loc = self.F_loc
                    temporary_loc[1] -= 1
                    if(temporary_loc == self.M_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "left"
                elif(direction == "right"):
                    temporary_loc = self.F_loc
                    temporary_loc[1] += 1
                    if(temporary_loc == self.M_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "right"
        elif (agent == "M"):
            for direction in possible_directions:
                if(direction == "up"):
                    temporary_loc = self.M_loc
                    temporary_loc[0] += 1
                    if(temporary_loc == self.F_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "up"
                elif(direction == "down"):
                    temporary_loc = self.M_loc
                    temporary_loc[0] -= 1
                    if(temporary_loc == self.F_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "down"
                elif(direction == "left"):
                    temporary_loc = self.M_loc
                    temporary_loc[1] -= 1
                    if(temporary_loc == self.F_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "left"
                elif(direction == "right"):
                    temporary_loc = self.M_loc
                    temporary_loc[1] += 1
                    if(temporary_loc == self.F_loc or (temporary_loc[0] < 0 or temporary_loc[0] > 5) or (temporary_loc[1] < 0 or temporary_loc[1] > 5)):
                        possible_directions -= "right"
        return possible_directions

    #Check to see if the game has reached final state
    def end_game(self):
        if(self.board == self.end_board):
            print("===============================Terminal State Reached=============")
            return True
        else:
            return False
    
    def render(self):
        print("Female location")
        print(self.F_loc)
        print("Male location")
        print(self.M_loc)

class Agent:
    def __init__(self, alpha, gamma):
        #Initiate agent depending on the sex
        self.current_loc = np.array([-1, -1])
        self.carrying = False

    #Prandom function call
    def Prandom(self, game, agent):
        if (agent == "F"):
            self.current_loc = game.F_loc
        elif (agent == "M"):
            self.current_loc = game.M_loc

        print(PICKUP)
        if (self.current_loc in PICKUP):
            game.board[self.current_loc] -= 1
            self.carrying = True
            print("testingpickup")
            return "pickup"

        elif (self.current_loc in DROP_OFF and self.carrying == True):
            game.board[self.current_loc] += 1
            self.carrying = False
            print("testingdrop")
            return "dropoff"

        else:
            possible_directions = ["up", "down", "left", "right"]
            choices = game.check_possible_action(agent, possible_directions)
            choice = np.random(choices)
            return choice



