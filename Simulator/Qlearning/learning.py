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

    # Declare and initialize variables
    Epsilon = 0
    LR = 0.01
    Gamma = 0.8

    Fairness_Threshold = 0.8
    n = 2

    states = [0, 1, 2, 3, 4, 5, 6,
              7, 8, 9,10,11,12,13,
             14,15,16,17,18,19,20]

    initial_state = 0   # Choose initial state between 0 to 6

    current_state = 0
    previous_state = 0

    current_frame = initial_state

    original_power = PARAMS().pTxLTE
    pFactor = [1,0.05,1.5]
    current_pFactor = 1

    possible_actions = [-1,0,1,-2,2]  # -1 to move backward
                                # 0 to stay there
                                # 1 to move forward
                                # -2 to move down
                                # +2 to move up

    current_action = None

    

    Q_Table = np.zeros([21,5],dtype = np.float64)



    def ChoosePtoDecideAction(self):
        p = round(random.uniform(0,1),4)
        return p

    # Function mapping fairness value to reward
    def FairnessToReward(self,Fairness,U_LTE,scene_params):
        if Fairness < self.Fairness_Threshold:
            reward_fx = ((self.Fairness_Threshold - Fairness)/((1/self.n)-self.Fairness_Threshold))*(1-U_LTE)
        else:
            reward_fx = ((Fairness - self.Fairness_Threshold)/0.2)*U_LTE
        
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

        if self.current_action !=2 and self.current_action !=-2: 
            self.current_state = self.current_state + self.current_action

            if self.current_state <= -1 and self.current_action == -1:
                self.current_state = 6

            elif self.current_state == 7 and self.current_action == 1:
                self.current_state = 0

            elif self.current_state == 6 and self.current_action == -1:
                self.current_state = 13
            
            elif self.current_state == 14 and self.current_action == 1:
                self.current_state = 7
            
            elif self.current_state == 13 and self.current_action == -1:
                self.current_state = 20

            elif self.current_state >= 21 and self.current_action == 1:
                self.current_state = 14
        
        elif self.current_action ==2 or self.current_action ==-2:

            if self.current_action ==-2:
                if self.current_state<=13:
                    self.current_state = self.current_state + 7
                else:
                    self.current_state = self.current_state % 7
            
            elif self.current_action ==2:
                if self.current_state>=7:
                    self.current_state = self.current_state - 7
                else:
                    self.current_state = self.current_state + 14

        self.current_frame = self.current_state % 7
        if self.current_state >= 0:
            self.current_pFactor = self.pFactor[0]
        if self.current_state >=7:
            self.current_pFactor = self.pFactor[1]
        if self.current_state >=14:
            self.current_pFactor = self.pFactor[2]

    def UpdateQtable(self,Fairness, U_LTE, scene_params):
        current_reward = self.FairnessToReward(Fairness, U_LTE ,scene_params)

        if self.current_action == -2:
            column = 3
        elif self.current_action == 2:
            column = 4
        else:
            column = self.current_action+1

        Q_s_a = self.Q_Table[self.previous_state][column]

        self.Q_Table[self.previous_state][column] = Q_s_a + self.LR*(self.Gamma * max(self.Q_Table[self.current_state]) + current_reward - Q_s_a)
