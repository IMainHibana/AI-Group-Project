import Demo

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



        #Exp 1:
        for i in range(0, 50):
            if (cur_turn == "F"):
                action = agent_F.Prandom(game, "F")
                
                reward += game.action("F", action)
                print(action)
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