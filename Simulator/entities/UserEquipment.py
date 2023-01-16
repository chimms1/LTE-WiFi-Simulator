import numpy as np
import math
from running.ConstantParams import PARAMS

class LTEUserEquipment:
    ueID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    powerRcvd_list = np.array([])  # List of Powers of BaseStations associated with this user
    bs = None # the BS to which this UE is connected. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    SINR = None
    LTEslotsreq=PARAMS().LTEslotsreq


    def getPowerRcvd(self,b):
        dist = float()
        dist = ((b.x-self.x)**2 + (b.y-self.y)**2 )**0.5

        pathloss = float()
        pathloss=20*math.log(2400,10)+30*math.log(dist,10)+19-28

        #Measure power
        prcvd = float()
        prcvd = PARAMS().get_dB_from_Watt(b.pTx) - pathloss

        return prcvd


    # Measure SINR from all Base Stations, Assign max BS to self UE and return index of max BS
    def measureSINRandConnect(self,lbss,wbss):

        maxsinr = -99999999
        maxind = 0
        ind = 0
        #================================================================
        sinr_list = []

        wifi_power_sum = 0
        for w in wbss:
            wifi_power_recv = self.getPowerRcvd(w)
            wifi_power_sum = wifi_power_sum + PARAMS().get_Watt_from_dB(wifi_power_recv)
        
        wifi_part = wifi_power_sum + PARAMS().get_mWatt_from_dBm(PARAMS().noise)
        

        for b in lbss:


            lte_power_rcvd = self.getPowerRcvd(b)
            sinr_temp = lte_power_rcvd-(PARAMS().get_dB_from_Watt(wifi_part))
            sinr_list.append(sinr_temp)

            if maxsinr <= sinr_temp:
                maxsinr = sinr_temp
                maxind = ind

            ind+=1

        self.bs = lbss[maxind]
        print(sinr_list)
        

        #================================================================
        # for b in bs_list:
        #     prcvd = self.getPowerRcvd(b)

        #     if maxpwr <= prcvd:
        #         maxpwr = prcvd
        #         maxind = ind

        #     #Add to the list
        #     self.powerRcvd_list = np.append(self.powerRcvd_list,prcvd)
        #     ind+=1
        
        # #ind = np.argmax(self.powerRcvd_list)
        # self.bs = bs_list[maxind]

        return maxind

    # User must be connected to a Base Station to use this function
    def measureSINR(self,wbss):

        wifi_power_sum = 0
        lte_power_rcvd = self.getPowerRcvd(self.bs)

        for w in wbss:
            wifi_power_recv = self.getPowerRcvd(w)
            wifi_power_sum = wifi_power_sum +PARAMS().get_Watt_from_dB( wifi_power_recv)
        
        wifi_power_sum = wifi_power_sum + PARAMS().get_mWatt_from_dBm(PARAMS().noise)
        
        self.SINR = lte_power_rcvd-(PARAMS().get_dB_from_Watt(wifi_power_sum))


class WifiUserEquipment:
    ueID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    powerRcvd_list = np.array([])  # List of users associated with this BaseStation
    bs = None # the BS to which this UE is connected. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    SNR = None
    probability = None
    wifislotsreq=PARAMS().wifislotsreq


    def getPowerRcvd(self,b):
        dist = float()
        dist = ((b.x-self.x)**2 + (b.y-self.y)**2 )**0.5

        pathloss = float()

        pathloss=20*math.log(2400,10)+30*math.log(dist,10)+19-28

        #Measure power
        prcvd = float()
        prcvd = PARAMS().get_dB_from_Watt(b.pTx) - pathloss

        return prcvd

    # Measure SNR from all Base Stations, Assign max BS to self UE and return index of max BS
    def measureSNRandConnect(self,lbss,wbss):

        maxsnr = -99999999
        maxind = 0
        ind = 0
        #================================================================
        snr_list = []

        for w in wbss:

            wifi_power_rcvd = self.getPowerRcvd(w)

            snr_temp = wifi_power_rcvd-(PARAMS().get_dB_from_dBm(PARAMS().noise))

            snr_list.append(snr_temp)

            if maxsnr <= snr_temp:
                maxsnr = snr_temp
                maxind = ind

            ind+=1

        self.bs = wbss[maxind]

        print(snr_list)

        

        #================================================================
        # for b in bs_list:
        #     prcvd = self.getPowerRcvd(b)

        #     if maxpwr <= prcvd:
        #         maxpwr = prcvd
        #         maxind = ind

        #     #Add to the list
        #     self.powerRcvd_list = np.append(self.powerRcvd_list,prcvd)
        #     ind+=1
        
        # #ind = np.argmax(self.powerRcvd_list)
        # self.bs = bs_list[maxind]

        return maxind

    # User must be connected to a Base Station to use this function
    def measureSNR(self):

        wifi_power_rcvd = self.getPowerRcvd(self.bs)

        self.SNR = wifi_power_rcvd-(PARAMS().get_dB_from_dBm(PARAMS().noise))