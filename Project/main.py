import itertools
import matplotlib
import matplotlib.style
import numpy as np
import pandas as pd
import sys

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








