from cmath import exp
import itertools
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
#import pyGame
import sys

class Game:
    Row = 5   
    Col = 5 
    INITIAL_STATE_M = (4, 2) #INITIAL STATE OF MALE AGENT
    INITIAL_STATE_F = (0, 2) #INITAL STATE OF FEMALE AGENT
    Locations = np.array([[0,0,0], [0,4,0], [2,2,0], [4,4,0], [3,1,10], [2,4,10]]) #LIST of all reward locations
    End_state = np.array([[0,0,5],[0,4,5],[2,2,5],[4,4,5], [3,1,0], [2,4,0]])   #End state of the game

    def __init__(self):
        #3D array board
        self.board = np.zeros([self.Row,self.Col,1])
        self.end_board = self.board.copy()

        #Hard coded pickup values into the board
        self.board[3, 1] = 10
        self.board[2, 4] = 10

        #Hard coded end_state board
        self.end_board[0,0] = 5
        self.end_board[0,4] = 5
        self.end_board[2,2] = 5
        self.end_board[4,4] = 5
        
        self.moves = ("up", "down", "left", "right", "pickup", "dropoff")

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
    
    def end_game(self):
        if(self.board == self.end_board):
            print("===============================Terminal State Reached=============")
            return True
        else:
            return False

class Agent:
    def __init__(self, sex, game, alpha, gamma):

    def Prandom(self, )


