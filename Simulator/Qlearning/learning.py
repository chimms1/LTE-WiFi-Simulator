# Initialize Q table
#     create a table(may be list) of 7 coumns and 3 rows
#           FS1 FS2 FS3 FS4 FS5 FS6 FS7
#     stay   -    -    -   -    -     -    
#     back   -    -    -   -    -     -     
#     front  -    -    -   -    -     -    -

# while
# choose current state
# choose random no p
#     if p<epsilon
#         action(a)=argmax Q(s,a)
#     else
#         choose random action
# perform action(a) calculate reward(run simulation and map fairness to get reward)
# update Q 
# current state=new state

import random
import numpy as np

from running.ConstantParams import PARAMS

class learning:
    # Create Q Table

    exploration = 10000

    # Declare and initialize variables
    Epsilon = 0
    LR = 0.01
    Gamma = 0.8

    Fairness_Threshold = 0.8
    n = 2

    states = [0,1,2,3,4,5,6]
    initial_state = 0

    current_state = 0
    previous_state = 0

    possible_actions = [-1,0,1]  # -1 to move backward
                                # 0 to stay there
                                # 1 to move forward

    current_action = None
    Q_Table = np.zeros([7,3],dtype = np.float64)



    def ChoosePtoDecideAction(self):
        p = round(random.uniform(0,1),4)
        return p

    # Function mapping fairness value to reward
    def FairnessToReward(self,Fairness,scene_params):
        if Fairness < self.Fairness_Threshold:
            reward_fx = (self.Fairness_Threshold - Fairness)/((1/self.n)-self.Fairness_Threshold)
        else:
            reward_fx = (Fairness - self.Fairness_Threshold)/0.2
        
        return reward_fx
    
    def getMaxAction(self):
        find = max(self.Q_Table[self.current_state])

        if self.Q_Table[self.current_state][0] == find:
            return -1

        if self.Q_Table[self.current_state][1] == find:
            return 0
        
        if self.Q_Table[self.current_state][2] == find:
            return 1

    # Function to choose action depending on Epsilon Greedy Algorithm (random number p and Epsilon)
    def ChooseAction(self,p):
        if p<self.Epsilon:
            # action(a)=argmax Q(s,a)
            self.current_action = self.getMaxAction()

        else:
            self.current_action = random.choice(self.possible_actions)
    
    # Function to perform the choosen action (modifies self.current_state variable)
    def PerformAction(self):
        # Goto the state given by action
        # (After this)
            # Run simulation on that frame
            # Calculate fairness and map it to reward
            # Update Q table
        self.previous_state = self.current_state
        self.current_state = self.current_state + self.current_action

        if self.current_state <= -1:
            self.current_state = 6

        if self.current_state >= 7:
            self.current_state = 0

    def UpdateQtable(self,Fairness,scene_params):
        current_reward = self.FairnessToReward(Fairness, scene_params)

        Q_s_a = self.Q_Table[self.previous_state][self.current_action+1]

        self.Q_Table[self.previous_state][self.current_action+1] = Q_s_a + self.LR*(self.Gamma * max(self.Q_Table[self.current_state]) + current_reward - Q_s_a)
