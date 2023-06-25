# Leaning class as per DynaQ+ algorithm
import random
import numpy as np
import math

from running.ConstantParams import PARAMS

class learning:

    exploration = 30000 # No. of iterations for exploration

    do_dyna = 0 # variable used in runtime, do not change

    # Declare and initialize variables
    k = 0.05
    Epsilon = 0 # epsilon value for exploration, exploitation epsilon is in main file
    LR = 0.05
    Gamma = 0.6

    Fairness_Threshold = 0.8
    U_LTE_Threshold = 0.8

    n = 2

    states = [[0, 1, 2, 3, 4, 5, 6],
              [7, 8, 9,10,11,12,13],
             [14,15,16,17,18,19,20]]
    

    initial_state = 0   # Choose initial state between 0 to 6

    current_state = 0
    state_i = current_state
    state_j = current_state
    
    previous_state = 0

    current_frame = initial_state


    original_power = PARAMS().pTxLTE

    
    pFactor = [1,1.05,1.10]
    power_levels = len(pFactor)

    current_pFactor = 1

    possible_actions = [-1,0,1,-2,2]  # -1 to move backward
                                # 0 to stay there
                                # 1 to move forward
                                # -2 to move down
                                # +2 to move up

    current_action = None

    

    Q_Table = np.zeros([21,5],dtype = np.float64)

    T_Count = np.zeros([21,5],dtype = np.int64)

    def ChoosePtoDecideAction(self):
        p = round(random.uniform(0,1),4)
        return p
    
    def MappingFairness(self,Fairness):

        if Fairness < self.Fairness_Threshold:
            reward_fx = (self.Fairness_Threshold - Fairness)/((1/self.n)-self.Fairness_Threshold)
        else:
            reward_fx = (Fairness - self.Fairness_Threshold)/0.2

        return reward_fx
    
    def MappingU_LTE(self,U_LTE):
        if U_LTE < self.U_LTE_Threshold:
            reward_ux = (U_LTE - self.U_LTE_Threshold) / self.U_LTE_Threshold
        else:
            reward_ux = (U_LTE - self.U_LTE_Threshold) / 0.2
        
        return reward_ux

    # Function mapping fairness and U_LTE value to reward
    def RewardFunction(self,Fairness,LTEPowerS,U_LTE,scene_params):
        
        # reward_fx = self.MappingFainess(Fairness)
        # reward_ux = self.MappingU_LTE(U_LTE)

        # return reward_fx*reward_ux
        # if Fairness < self.Fairness_Threshold:
        #     reward_fx = ((self.Fairness_Threshold - Fairness)/((1/self.n)-self.Fairness_Threshold))*(1-U_LTE)
        # else:
        #     reward_fx = ((Fairness - self.Fairness_Threshold)/0.2)*U_LTE
        
        # return reward_fx

        zeroes = {0:2,1:4,2:6,3:6,4:7,5:8,6:3}

        energy = LTEPowerS/(200*zeroes[self.current_frame]*PARAMS().pTx_one_PRB)

        # if U_LTE <1:
        #     reward = self.MappingFairness(Fairness)/(LTEPowerS*(1-U_LTE))
        # else:
        #     reward = self.MappingFairness(Fairness)/(LTEPowerS*(1-0.999999))

        reward = (self.MappingFairness(Fairness)/LTEPowerS)

        # fairness_weight = 0.3
        # utilization_weight = 0.2
        # power_consumption_weight = 0.5

        # fairness_normalized = (self.MappingFairness(Fairness) + 1) / 2  # Normalize fairness to the range [0, 1]
        # utilization_normalized = U_LTE
        # power_consumption_normalized = (0.00152 - LTEPowerS) / (0.00152 - 0.0000008636363635)  # Normalize power consumption to the range [0, 1]

        # reward = (fairness_normalized * fairness_weight) + (utilization_normalized * utilization_weight) + (power_consumption_normalized * power_consumption_weight)



        # reward = self.MappingFairness(Fairness)

        return reward

    def RewardBonusDynaQ(self):

        # t = max(self.T_Count[self.previous_state])
        if self.current_action == -2:
            column = 3
        elif self.current_action == 2:
            column = 4
        else:
            column = self.current_action+1

        t = self.T_Count[self.previous_state][column]

        return (self.k * math.sqrt(t))
    
    def getMaxAction(self):

        find = max(self.Q_Table[self.current_state])

        if self.Q_Table[self.current_state][0] == find:
            return -1

        if self.Q_Table[self.current_state][1] == find:
            return 0
        
        if self.Q_Table[self.current_state][2] == find:
            return 1
        
        if self.Q_Table[self.current_state][3] == find:
            return -2
        
        if self.Q_Table[self.current_state][4] == find:
            return 2

    def getMaxActionInd(self):
        find = max(self.Q_Table[self.current_state])

        if self.Q_Table[self.current_state][0] == find:
            return 0

        if self.Q_Table[self.current_state][1] == find:
            return 1
        
        if self.Q_Table[self.current_state][2] == find:
            return 2
        
        if self.Q_Table[self.current_state][3] == find:
            return 3
        
        if self.Q_Table[self.current_state][4] == find:
            return 4
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

            # self.current_state = self.current_state + self.current_action
            self.state_i = self.state_i + self.current_action


            if self.state_i > len(self.states[0])-1:
                self.state_i = 0
            
            elif self.state_i < 0:
                self.state_i = len(self.states[0])-1
        
        else:

            self.state_j = self.state_j - int(self.current_action/2)

            if self.state_j > self.power_levels-1:
                self.state_j = 0
            
            elif self.state_j < 0:
                self.state_j = self.power_levels-1
            
        self.current_state = self.states[self.state_j][self.state_i]
        self.current_frame = self.state_i
        self.current_pFactor = self.pFactor[self.state_j]

    def UpdateQtable(self,Fairness, LTEPowerS, U_LTE, scene_params,current_iteration):

        if current_iteration>self.exploration and self.do_dyna == 1:
            
            current_reward = self.RewardFunction(Fairness, LTEPowerS, U_LTE, scene_params)
            
            if current_reward<=0:
                current_reward -= self.RewardBonusDynaQ()
            else:
                current_reward += self.RewardBonusDynaQ()
        
        
        else:
            current_reward = self.RewardFunction(Fairness, LTEPowerS, U_LTE, scene_params)
        
        # print(Fairness,current_reward)

        if self.current_action == -2:
            column = 3
        elif self.current_action == 2:
            column = 4
        else:
            column = self.current_action+1

        Q_s_a = self.Q_Table[self.previous_state][column]

        self.Q_Table[self.previous_state][column] = Q_s_a + self.LR*(self.Gamma * max(self.Q_Table[self.current_state]) + current_reward - Q_s_a)

    def UpdateT_Count(self):

        # for t in range(0,len(self.possible_actions)):
        #     self.T_Count[self.current_state][t] += 1

        self.T_Count += 1

        self.T_Count[self.current_state][self.current_action] = 0
        
