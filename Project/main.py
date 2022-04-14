import itertools
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import random

import sys
ROWS = 5   #ROWS IN WORLD
COLS = 5 #COLUMNS IN WORLD
INITIAL_STATE_M = (5, 3) #INITIAL STATE OF MALE AGENT
INITIAL_STATE_F = (1, 3) #INITAL STATE OF FEMALE AGENT
PICKUP=[(3, 5), (4, 2)] #LIST OF PICKUP STATES
DROP_OFF = [(1, 1), (1, 5), (3, 3), (5, 5)] #LIST OF DROP OFF STATES
DETERMINISTIC = False
#easier to make the states a class instead of a regular self susteining function
# our grid as a 2d array
grid = np.zeros((ROWS, COLS), dtype='i,i')
for i in range(0, ROWS):
    for j in range(0, COLS):
        grid[i][j] = (i+1, j+1)

print(grid)
class State:  #class for the states, to have a better idea of how they're being maintained
    def __init__(self, state=INITIAL_STATE_M):
        self.board = np.zeros([ROWS,COLS])
        self.board[1,1] = -1
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC
    def giveReward(self):       #adds the rewards to each state
        if self.state in DROP_OFF:
            return 13
        if self.state in PICKUP:
            return 13
        else:
            return -1
    def isinDropOff(self):   #this helps to know if an agent has the ability to drop or not
        if (self.state in DROP_OFF):
            self.canDrop = True
    def isinPickUp(self):    #this helps to know if an agent can pick up or not
        if (self.state in PICKUP):
            self.canPickUp = True

    def chooseActionProb(self, action):   #makes the probability of the actions knowable
        if action == "up":
            return np.random.choice(["up", "left", "right"], p=[0.8, 0.1, 0.1])
        if action == "down":
            return np.random.choice(["down", "left", "right"], p=[0.8, 0.1, 0.1])
        if action == "left":
            return np.random.choice(["left", "up", "down"], p=[0.8, 0.1, 0.1])
        if action == "right":
            return np.random.choice(["right", "up", "down"], p=[0.8, 0.1, 0.1])

    # THE NEXT POSITION FOR OUR AGENT
    def nextPosition(self, action): #helps to determine next action of the agent
        if self.determine:
            if action == "up":
                nextState = (self.state[0] - 1, self.state[1])
            elif action == "down":
                nextState = (self.state[0] + 1, self.state[1])
            elif action == "left":
                nextState = (self.state[0], self.state[1] - 1)
            else:
                nextState = (self.state[0], self.state[1] + 1)
            self.determine = False
        else:
            action = self.chooseActionProb(action)
            self.determine = True
            nextState = self.nextPosition(action)

        if (nextState[0] >= 0) and (nextState[0] <= 2):
            if (nextState[1] >= 0) and (nextState[1] <= 3):
                if nextState != (1, 1):
                    return nextState
        return self.state
    def displayBoard(self):   #displays the board
        self.board[self.state] = 1
        for i in range(0, ROWS):
            print('-------------------')
            out = '| '
            for j in range(0, COLS):
                if self.board[i,j] == 1:
                    token ='*'
                if self.board[i,j] == -1:
                     token = 'z'
                if self.board[i, j] == 0:
                    token ='0'
                out += token + ' | '
            print(out)
        print('------------------------')


class Agent:
    def __init__(self):
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.isinDropOff = self.State.isinDropOff
        self.isinPickup = self.State.isinPickUp
        self.alpha = 0.3
        self.gamma = 0.5
        self.exp_rate = 0.3

        self.Q_Values = {}
        for i in range (ROWS):
            for j in range(COLS):
                self.Q_Values[(i,j)] = {}
                for n in self.actions:
                    self.Q_Values[(i,j)][n] = 0

    def chooseAct(self):
        maxReward = 0
        action = ""

        if np.random.uniform(0,1)<=self.exp_rate:
            action = np.random.choice(self.actions)
        else:

            for n in self.actions:
                current_position = self.State.state
                reward = self.Q_Values[current_position][n]
                if reward >= maxReward:
                    action = n
                    maxReward = reward
            return action







def EpsillonGreedyPolicy(Q,epsilon,num_actions):

    #yes I used gfg
    def policyFunction(state):
        action_probabilities = np.ones(num_actions, dtype=float) * epsilon/num_actions
        best_action = np.argmax(Q[state])
        action_probabilities[best_action] += (1.0 -epsilon)
        return action_probabilities
    return policyFunction

 








