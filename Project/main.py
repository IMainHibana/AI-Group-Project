import itertools
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import pyGame
import sys

ROWS = 5   #ROWS IN WORLD
COLS = 5 #COLUMNS IN WORLD
INITIAL_STATE_M = (5, 3) #INITIAL STATE OF MALE AGENT
INITIAL_STATE_F = (1, 3) #INITAL STATE OF FEMALE AGENT
PICKUP=[(3, 5), (4, 2)] #LIST OF PICKUP STATES
DROP_OFF = [(1, 1), (1, 5), (3, 3), (5, 5)] #LIST OF DROP OFF STATES
DETERMINISTIC = False
#easier to make the states a class instead of a regular self sustaining function

# our grid as a 2d array
grid = np.zeros((ROWS, COLS), dtype='i,i')
for i in range(0, ROWS):
    for j in range(0, COLS):
        grid[i][j] = (i+1, j+1)

class State:  #class for the states, to have a better idea of how they're being maintained
    def __init__(self, state=INITIAL_STATE_M):
        self.board = np.zeros([ROWS,COLS])
        self.board[1,1] = -1
        self.state = state
        self.canDrop = False
        self.canPickUp = False
        self.isEnd = False
        self.determine = DETERMINISTIC
        #self.State.state prints out the position in the grid
    def giveReward(self):       #adds the rewards to each state
        if self.state in DROP_OFF:
            return 13     #if in a DROPOFF space, reward the agent 13
        if self.state in PICKUP:
            return 13  #if the dropoff is in a pickup space, reward the agent 13
        else:
            return -1 #if in any other space thats not dropoff/pickup, give the agent -1
    def isinDropOff(self):   #this helps to know if an agent has the ability to drop or not
        if (self.state in DROP_OFF):
            self.canDrop = True
    def isinPickUp(self):    #this helps to know if an agent can pick up or not
        if (self.state in PICKUP):
            self.canPickUp = True

    def chooseActionProb(self, action):   #makes the probability of the actions knowable
        if action == "up":
            return np.random.choice(["up", "left", "right"], p=[0.8, 0.1, 0.1])   #the opposite action doesn't occur since we'd
                                                                                  #just go back to the same space and get nowhere
        if action == "down":
            return np.random.choice(["down", "left", "right"], p=[0.8, 0.1, 0.1])
        if action == "left":
            return np.random.choice(["left", "up", "down"], p=[0.8, 0.1, 0.1])
        if action == "right":
            return np.random.choice(["right", "up", "down"], p=[0.8, 0.1, 0.1])

    # THE NEXT POSITION FOR OUR AGENT
    def nextPosition(self, action): #helps to determine next action of the agent
        if self.determine:
            #the following stores the next state into nextState, as a tuple
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
            #if non-deterministic at the moment, as in the action is random or in multiple possible states at the same time
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
    def takeAct(self,action):
        pos = self.State.nextPosition(action)
        return State(state=pos)
    def end(self):
        self.states=[]
        self.State = State()

        return True
        #need to add an end condition here
    def test(self, rounds = 10):
        n = 0
        while n < rounds:
            if self.State.isEnd:
                reward = self.State.giveReward()
                for a in self.actions:
                    self.Q_Values[self.State.state][a] = reward
                print("End Reward: ", reward)
                for s in reversed(self.states):
                    current_q_val = self.Q_Values[s[0]][s[1]]
                    reward = current_q_val + self.lr * (self.gamma*reward - current_q_val)
                    self.Q_Values[s[0]][s[1]] = round(reward, 3)
                self.end()
                n+=1
            else:
                action = self.chooseAct()
                self.states.append([(self.State.state), action])
                print("Location {} action {}".format(
                    self.State.state, action))
                self.State = self.takeAct(action)
                self.State.isinDropOff()
                print("next state is: ", self.State.state)
                self.isEnd = self.State.isEnd


def EpsillonGreedyPolicy(Q,epsilon,num_actions):

    #yes I used gfg
    def policyFunction(state):
        action_probabilities = np.ones(num_actions, dtype=float) * epsilon/num_actions
        best_action = np.argmax(Q[state])
        action_probabilities[best_action] += (1.0 -epsilon)
        return action_probabilities
    return policyFunction

def Prandom(dropoff, pickup):
    #Pass in dropoff and pickup state (true or false)
    if(dropoff == True):
        pass
    elif(pickup == True):
        pass
    else:
        pass
class main():
# our visualization using pygame
    
    male = Agent()

    #pyGame.pyGameGrid()




