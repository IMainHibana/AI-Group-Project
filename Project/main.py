import Demo
import numpy as np

class main():
    def Run():
        #Declaring every game initial state and value
        alpha = 0.3
        gamma = 0.5
        exp_rate = 0.3
        cur_turn = "F"
        reward = 0

        game = Demo.Game()
        agent_F = Demo.Agent(alpha, gamma)
        agent_M = Demo.Agent(alpha, gamma)

        q_table = [
            [0,0], [0,0], [0,0], [0,0], [0,0],
            [0,0], [0,0], [0,0], [0,0], [0,0],
            [0,0], [0,0], [0,0], [0,0], [0,0],
            [0,0], [0,0], [0,0], [0,0], [0,0],
            [0,0], [0,0], [0,0], [0,0], [0,0]
        ]

        reward_matrix = [
            [13,0], [0,0], [0,0], [0,0], [13,0],
            [0,0], [0,0], [0,0], [0,0], [0,0],
            [0,0], [0,0], [13,0], [0,0], [13,0],
            [0,0], [13,0], [0,0], [0,0], [0,0],
            [0,0], [0,0], [0,0], [0,0], [13,0]
        ]

        pick_drop_states = [2, 4], [3, 1], [0, 0], [0, 4], [2, 2], [4, 4]

        def getAllPossibleNextAction(cur_pos):
            step_matrix = [x != None for x in reward_matrix[cur_pos]]
            action = []
            if (step_matrix[0]):
                action.append(0)
            if(step_matrix[1]):
                action.append(1)
            return(action)

        def isGoalStateReached(cur_pos):
            return (cur_pos in [6])

        # Exp 1:
        for i in range(0, 500):
            print("=======================================new turn===================================================")
            if (cur_turn == "F"):
                action = agent_F.Prandom(game, "F")
                
                reward += game.action("F", action)
                #print(action)
                game.render()
               
                if(game.end_game()):
                    print("HAS REACHED THE END GAME")
                    return
                cur_turn = "M"
            elif (cur_turn == "M"):
                action = agent_M.Prandom(game, "M")
                reward += game.action("M", action)
                print(action)
                game.render()
                if(game.end_game()):
                    print("HAS REACHED THE END GAME")
                    return
                cur_turn = "F"

    Run()