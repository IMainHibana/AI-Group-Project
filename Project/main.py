import itertools
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import sys
ROWS = 5   #ROWS IN WORLD
COLS = 5 #COLUMNS IN WORLD
INITIAL_STATE_M = (5, 3) #INITIAL STATE OF MALE AGENT
INITIAL_STATE_F = (1, 3) #INITAL STATE OF FEMALE AGENT
PICKUP=[(3, 5), (4, 2)] #LIST OF PICKUP STATES
DROP_OFF = [(1, 1), (1, 5), (3, 3), (5, 5)] #LIST OF DROP OFF STATES
DETERMINISTIC = False



#FUNCTION THAT WILL REWARD OUR AGENT WHEN DOING SOMETHING RIGHT/WRONG
def giveReward(self):
    if self.state in DROP_OFF:
        return 1
    elif self.state in PICKUP:
        return -1
    else:
        return 0

def chooseActionProb(self, action):
    if action == "up":
        return np.random.choice(["up", "left", "right"], p=[0.8, 0.1, 0.1])
    if action == "down":
        return np.random.choice(["down", "left", "right"], p=[0.8, 0.1, 0.1])
    if action == "left":
        return np.random.choice(["left", "up", "down"], p=[0.8, 0.1, 0.1])
    if action == "right":
        return np.random.choice(["right", "up", "down"], p=[0.8, 0.1, 0.1])



#THE NEXT POSITION FOR OUR AGENT
def nextPosition(self, action):
    if self.determine:
        if action =="up":
            nextState=(self.state[0]-1, self.state[1])
        elif action == "down":
            nextState = (self.state[0]+1, self.state[1])
        elif action == "left":
            nextState = (self.state[0], self.state[1]-1)
        else:
            nextState = (self.state[0], self.state[1]+1)
        self.determine = False
    else:
        action = self.chooseActionProb(action)
        self.determine = True
        nextState = self.nextPosition(action)


    if(nextState[0] >= 0) and (nextState[0]<=2):
        if (nextState[1] >= 0) and (nextState[1]<=3):
            if nextState != (1,1):
                return nextState
    return self.state


def EpsillonGreedyPolicy(Q,epsilon,num_actions):

    #yes I used gfg
    def policyFunction(state):
        action_probabilities = np.ones(num_actions, dtype=float) * epsilon/num_actions
        best_action = np.argmax(Q[state])
        action_probabilities[best_action] += (1.0 -epsilon)
        return action_probabilities
    return policyFunction

 
def agent():
    #can move north, south, east, west
    #can pickup something
    #can dropoff something
    #CANNOT OCCUPY THE SAME STATE AS ANOTHER AGENT
    return








