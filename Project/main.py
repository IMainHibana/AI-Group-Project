from cmath import exp
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
INITIAL_STATE_M = (4, 2) #INITIAL STATE OF MALE AGENT
INITIAL_STATE_F = (0, 2) #INITAL STATE OF FEMALE AGENT
PICKUP=[(2, 4), (3, 1)] #LIST OF PICKUP STATES
DROP_OFF = [(0, 0), (0, 4), (2, 2), (4, 4)] #LIST OF DROP OFF STATES
PICKUP_MAX_QUANT = 10
DROP_OFF_MAX_QUANT = 5

#easier to make the states a class instead of a regular self sustaining function

#initiate the game board for each experiment
class Game:
    def __init__(self, experiment):
        #Initialized starting variables for an empty board
        self.board = np.zeros([ROWS,COLS])

        #Track the current boxes inside of each pickup/dropoff location
        self.drop_loc1 = 0  #0,0
        self.drop_loc2 = 0  #0,4
        self.drop_loc3 = 0  #2,2
        self.drop_loc4 = 0  #4,4
        self.pick_loc1 = PICKUP_MAX_QUANT   #2,4
        self.pick_loc2 = PICKUP_MAX_QUANT   #3,1

        self.isEnd = False

        self.male = Agent(INITIAL_STATE_M)      #Create two agents M and F
        self.female = Agent(INITIAL_STATE_F)
        self.male.opposite_agent_loc = self.female.current_pos
        self.female.opposite_agent_loc = self.male.current_pos
        turn = "Female"

    def Run(self, experiment):
        #Running experiment 1a
        if (experiment == "1a"):
            #Alternating turns between female and male
            for i in range(0, 500):
                if(turn == "Female"):
                    Prandom(self.female)
                    self.drop_action(self.female.current_pos)
                    self.pickup_action(self.female.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Male"
                elif(turn == "Male"):
                    Prandom(self.male)
                    self.drop_action(self.male.current_pos)
                    self.pickup_action(self.male.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Female"

            for i in range(0, 7500):
                if(turn == "Female"):
                    Prandom(self.female)
                    self.drop_action(self.female.current_pos)
                    self.pickup_action(self.female.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Male"
                elif(turn == "Male"):
                    Prandom(self.male)
                    self.drop_action(self.male.current_pos)
                    self.pickup_action(self.male.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Female"
        
        elif (experiment == "1b"):
            for i in range(0, 500):
                if(turn == "Female"):
                    Prandom(self.female)
                    self.drop_action(self.female.current_pos)
                    self.pickup_action(self.female.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Male"
                elif(turn == "Male"):
                    Prandom(self.male)
                    self.drop_action(self.male.current_pos)
                    self.pickup_action(self.male.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Female"
            for i in range(0, 7500):
                if(turn == "Female"):
                    Pgreedy(self.female)
                    self.drop_action(self.female.current_pos)
                    self.pickup_action(self.female.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Male"
                elif(turn == "Male"):
                    Pgreedy(self.male)
                    self.drop_action(self.male.current_pos)
                    self.pickup_action(self.male.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Female"

        elif (experiment == "1c"):
            for i in range(0, 500):
                if(turn == "Female"):
                    Prandom(self.female)
                    self.drop_action(self.female.current_pos)
                    self.pickup_action(self.female.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Male"
                elif(turn == "Male"):
                    Prandom(self.male)
                    self.drop_action(self.male.current_pos)
                    self.pickup_action(self.male.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Female"
            for i in range(0, 7500):
                if(turn == "Female"):
                    Pexploit(self.female)
                    self.drop_action(self.female.current_pos)
                    self.pickup_action(self.female.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Male"
                elif(turn == "Male"):
                    Pexploit(self.male)
                    self.drop_action(self.male.current_pos)
                    self.pickup_action(self.male.current_pos)
                    if(self.isEnd == True):
                        break
                    turn = "Female"

    
    def pickup_action(self, location):
        if(location == (2,4)):
            self.pick_loc1 -= 1
        elif(location == (3, 1)):
            self.pick_loc2 -= 1

    def drop_action(self, location):
        if(location == (0, 0)):
            self.drop_loc1 += 1
        elif(location == (0, 4)):
            self.drop_loc2 += 1
        elif(location == (2, 2)):
            self.drop_loc2 -= 1
        elif(location == (4, 4)):
            self.drop_loc2 -= 1
    
    def check_end(self):
        if(self.drop_loc1 == 5 and self.drop_loc2 == 5 and self.drop_loc3 == 5 and self.drop_loc4 == 5 and self.pick_loc1 == 0 and self.pick_loc2 == 0):
            self.isEnd = True

#Agent class used for both male and female, differentiate between the two by the starting initial state
class Agent:
    def __init__(self, initial_state):
        #Initialized all starting variables for any agent
        self.all_actions = []
        self.opposite_agent_loc = (-1, -1)
        self.current_pos = initial_state
        self.score = 0
        self.carrying = False

        self.Q_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.Q_values[(i, j)] = {}
                for a in self.actions:
                    self.Q_values[(i, j)][a] = 0 

        #Each agent have a set of possible actions from the Action class
        self.possible_action = Action(self)

#Contain all possible action an agent could take
class Action:  
    def __init__(self, agent):
        pass

    def giveReward(self, drop_or_pick, agent):       #adds the rewards to each state
        if (drop_or_pick == "Dropoff"):
            agent.carrying = False
            agent.score += 13     #if in a DROPOFF space, reward the agent 13
        if (drop_or_pick == "Pickup"):
            agent.carrying = True

            agent.score += 13  #if the dropoff is in a pickup space, reward the agent 13
        else:
            agent.score -= 1 #if in any other space thats not dropoff/pickup, give the agent -1

    #Agent choose the next action to take
    def chooseActionProb(self, action, agent):   
        if action == "up":
            self.nextPosition(action, agent)  
            agent.all_actions.append("up") 
                                                                                  
        elif action == "down":
            self.nextPosition(action, agent)  
            agent.all_actions.append("down")
        elif action == "left":
            self.nextPosition(action, agent) 
            agent.all_actions.append("left") 

        elif action == "right":
            self.nextPosition(action, agent) 
            agent.all_actions.append("right")

    def chooseAction(self, Agent):
      

    #Actually checking to see if the future action is overlaping with other agent or out of range
    #If not then action is initiated and recorded
    def nextPosition(self, action, agent): 
        temporary = agent.current_pos
        if action == "up":
            temporary = (temporary[0] - 1, temporary[1])
            if (self.check_cross_agent_loc(agent, temporary) and 0 <= temporary[0] ):
                agent.current_pos = temporary
                return True
            else:
                return False

        elif action == "down":
            temporary = (temporary[0] + 1, temporary[1])
            if (self.check_cross_agent_loc(agent, temporary) and temporary[0] <= 5):
                agent.current_pos = temporary
                return True
            else:
                return False

        elif action == "left":
            temporary = (temporary[0], temporary[1] - 1)
            if (self.check_cross_agent_loc(agent, temporary) and 0 <= temporary[1] ):
                agent.current_pos = temporary
                return True
            else:
                return False

        elif action == "right":
            temporary = (temporary[0], temporary[1] + 1)
            if (self.check_cross_agent_loc(agent, temporary) and temporary[1] <= 5):
                agent.current_pos = temporary
                return True
            else:
                return False
    
    #Cross check current agent future position and other agent current position
    def check_cross_agent_loc(self, agent, next_pos):
        if (agent.opposite_agent_loc != next_pos):
            return True
        else:
            return False

    
#First policy if pickup and dropoff is available activate those actions, if not pick an action randomly.
def Prandom(agent):
    agent_action = agent.possible_action
    #Check to see if location is in pickup or drop off
    if(agent.current_pos in DROP_OFF):
        #If in drop off location do drop off
        agent_action.giveReward("Dropoff", agent)
        
        #And then try to make the next move
        agent_action.giveReward("None", agent)
        possible_directions = ["up", "down", "left", "right"]
        choice = np.random.choice(possible_directions)
        #If the next move is overlaping with the other agent, cancel the move and do it again without the option to move to that location
        if(agent_action.chooseActionProb(choice, agent)):
            pass
        else:
            possible_directions.remove(choice)
            choice = np.random.choice(possible_directions)
            agent_action.chooseActionProb(choice, agent)

    elif(agent.current_pos in PICKUP):
        #If in pickup location, do pickup
        agent_action.giveReward("Pickup", agent)

        #And then try to make the next move
        agent_action.giveReward("None", agent)
        possible_directions = ["up", "down", "left", "right"]
        choice = np.random.choice(possible_directions)
        #If the next move is overlaping with the other agent, cancel the move and do it again without the option to move to that location
        if(agent_action.chooseActionProb(choice, agent)):
            pass
        else:
            possible_directions.remove(choice)
            choice = np.random.choice(possible_directions)
            agent_action.chooseActionProb(choice, agent)

    else:
        #If not in pickup location nor drop off location just make the next move
        agent_action.giveReward("None", agent)
        possible_directions = ["up", "down", "left", "right"]
        choice = np.random.choice(possible_directions)
        #If the next move is overlaping with the other agent, cancel the move and do it again without the option to move to that location
        if(agent_action.chooseActionProb(choice, agent)):
            pass
        else:
            possible_directions.remove(choice)
            choice = np.random.choice(possible_directions)
            agent_action.chooseActionProb(choice, agent)

#Second policy 
def Pexploit(agent):
    pass

#Third policy
def Pgreedy(agent):
    pass

class main():
    #Choose the first experiment
    game_1a = Game("1a")
    female_all_moves = game_1a.female.all_actions
    male_all_moves = game_1a.male.all_actions
    print("Female moves:")
    print(female_all_moves)
    print("Male moves:")
    print(male_all_moves)


# our visualization using pygame
pyGame.pyGameGrid(main.female_all_moves, main.male_all_moves)


    

