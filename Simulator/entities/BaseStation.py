import numpy as np
from running.ConstantParams import PARAMS

class LTEBaseStation:
    bsID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    pTx: int    # Transmission Power in watt
    #user_list: list[UserEquipment]  # List of users associated with this BaseStation
    user_list = np.array([])  # List of users associated with this BaseStation. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    SINR=None
    


    # def measureSINR(self,wbss):

    #     wifi_power_sum = 0
    #     for w in wbss:
    #         wifi_power_recv = w.pTx/((self.x - w.x)**2 + (self.y - w.y)**2)**0.5
    #         wifi_power_sum = wifi_power_sum + wifi_power_recv
        
    #     self.SINR = (self.pTx)/(PARAMS().noise + wifi_power_sum)

class WifiBaseStation:
    bsID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    pTx: int    # Transmission Power in watt
    #user_list: list[UserEquipment]  # List of users associated with this BaseStation
    user_list = np.array([])  # List of users associated with this BaseStation. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    SNR=None

    # def measureSNR(self):

    #     self.SNR = (self.pTx)/(PARAMS().noise)