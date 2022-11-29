import numpy as np
import math
from running.ConstantParams import PARAMS


class LTEUserEquipment:
    ueID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    powerRcvd_list = np.array([])  # List of users associated with this BaseStation
    # bs: BaseStation  # the BS to which this UE is connected
    bs = None # the BS to which this UE is connected. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    SINR = None


    def getPowerRcvd(self,b):
        dist = float()
        dist = ((b.x-self.x)**2 + (b.y-self.y)**2 )**0.5

        pathloss = float()
        pathloss=20*math.log(2400,10)+30*math.log(dist,10)+30-28

        #Measure power
        prcvd = float()
        prcvd = PARAMS().get_dB_from_Watt(b.pTx) - pathloss

        return prcvd


    # Measure Power Recieved from all Base Stations, Assign max BS to self UE and return index of max BS
    def measurePowerRcvd(self,bs_list):

        maxpwr = -99999999
        maxind = 0
        ind = 0

        for b in bs_list:
            prcvd = self.getPowerRcvd(b)

            if maxpwr <= prcvd:
                maxpwr = prcvd
                maxind = ind

            #Add to the list
            self.powerRcvd_list = np.append(self.powerRcvd_list,prcvd)
            ind+=1
        
        #ind = np.argmax(self.powerRcvd_list)
        self.bs = bs_list[maxind]

        return maxind

    # User must be connected to a Base Station to use this function
    def measureSINR(self,wbss):

        if(self.bs==None):
            print("User Not Connected to a BS to get SINR")
            return

        prcvd = self.getPowerRcvd(self.bs)

        wifi_power_sum = 0
        lte_power_rcvd = self.getPowerRcvd(self.bs)

        for w in wbss:
            wifi_power_recv = self.getPowerRcvd(w)
            wifi_power_sum = wifi_power_sum + wifi_power_recv
        
        self.SINR = lte_power_rcvd/(PARAMS().get_dB_from_dBm(PARAMS().noise) + wifi_power_sum)


class WifiUserEquipment:
    ueID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    powerRcvd_list = np.array([])  # List of users associated with this BaseStation
    bs = None # the BS to which this UE is connected. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    SNR = None
    probability=None

    def getPowerRcvd(self,b):
        dist = float()
        dist = ((b.x-self.x)**2 + (b.y-self.y)**2 )**0.5

        pathloss = float()
        pathloss=20*math.log(2400,10)+30*math.log(dist,10)+30-28

        #Measure power
        prcvd = float()
        prcvd = PARAMS().get_dB_from_Watt(b.pTx) - pathloss

        return prcvd

    # Measure Power Recieved from all Base Stations, Assign max BS to self UE and return index of max BS
    def measurePowerRcvd(self,bs_list):

        maxpwr = -99999999
        maxind = 0
        ind = 0

        for b in bs_list:

            prcvd = self.getPowerRcvd(b)

            if maxpwr <= prcvd:
                maxpwr = prcvd
                maxind = ind

            #Add to the list
            self.powerRcvd_list = np.append(self.powerRcvd_list,prcvd)
            ind+=1
        
        #ind = np.argmax(self.powerRcvd_list)
        self.bs = bs_list[maxind]

        return maxind

    # User must be connected to a Base Station to use this function
    def measureSNR(self):

        if(self.bs==None):
            print("User Not Connected to a BS to get SNR")
            return

        wifi_power_rcvd = self.getPowerRcvd(self.bs)
        self.SNR = wifi_power_rcvd/(PARAMS().get_dB_from_dBm(PARAMS().noise))

   

            



