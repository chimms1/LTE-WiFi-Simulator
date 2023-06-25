import numpy as np
import math
import random
from running.ConstantParams import PARAMS

class LTEUserEquipment:
    ueID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    powerRcvd_list = np.array([])  # List of Powers of BaseStations associated with this user
    bs = None # the BS to which this UE is connected. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    SINR = None

    req_data_rate = None # required data rate in Kbps
    req_bits_per_slot = None

    req_no_PRB = None   # total PRB required by user = (required bits per slot)
            #                           /(bits per symbol)*(total symbols in PRB)
    
    bits_sent = 0
    
    transmission_finished = 0




    def getPowerRcvd(self,b):
        dist = float()
        dist = ((b.x-self.x)**2 + (b.y-self.y)**2 )**0.5

        pathloss = float()
        pathloss=20*math.log(2400,10)+30*math.log(dist,10)+0-28

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
        # print(sinr_list)
        

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

        given_sinr = list(PARAMS().LTE_MCS.keys())

        if maxsinr < given_sinr[0]:
            print("Deleting user with SINR: ",maxsinr)
            return maxind

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
    probability = None  # Probability with which the user transmits
    # wifislotsreq = None
    
    req_data_rate = None # required data rate in Kbps
    req_bits_per_slot = None
    
    req_no_wifi_slot = None   # total wifi slots required by user = (required bits per wifi slot)
    #                                                               / (bits per wifi slot)
    random_backoff_slots = 0
    random_backoff_flag = 0
    # busy_count = 0

    DIFS_flag = 0
    DIFS_slots = PARAMS().DIFS_slots

    RTS_flag=0

    bits_sent = 0

    def getPowerRcvd(self,b):
        dist = float()
        dist = ((b.x-self.x)**2 + (b.y-self.y)**2 )**0.5

        pathloss = float()

        pathloss=20*math.log(2400,10)+30*math.log(dist,10)+0-28

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

        # print(snr_list)

        

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

        # given_snr = list(PARAMS().wifi_MCS.keys())

        # if maxsnr < given_snr[0]:
        #     print("Deleting user with SNR: ",maxsnr)
        #     return -1

        return maxind

    # User must be connected to a Base Station to use this function
    def measureSNR(self):

        wifi_power_rcvd = self.getPowerRcvd(self.bs)

        self.SNR = wifi_power_rcvd-(PARAMS().get_dB_from_dBm(PARAMS().noise))
    
    # sets a random backoff value in terms of number of slots
    def setRandomBackoff(self):
        self.random_backoff_slots = random.randint(PARAMS().backoff_lower, PARAMS().backoff_upper)