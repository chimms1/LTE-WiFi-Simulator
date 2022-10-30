import random
import math
import numpy as np
import pandas as pd
from running.ConstantParams import PARAMS
from entities.BaseStation import LTEBaseStation
from entities.BaseStation import WifiBaseStation
from entities.UserEquipment import LTEUserEquipment
from entities.UserEquipment import WifiUserEquipment

class ServiceClass:

    # Returns List of Base Stations of size PARAMS.numofLTEBS
    # each BS with a sequential ID and random location in (length,breadth)
    # If there is one BS then assign static location
    def createLTEBaseStations(self):
        
        bss = np.array([])

        if(PARAMS().numofLTEBS==1):
            b = LTEBaseStation()

            b.bsID = 1
            b.x = PARAMS().length/2
            b.y = PARAMS().breadth/2
            b.pTx = PARAMS().pTxLTE  # Watts

            bss = np.append(bss,b)

            return bss

        #bss = np.empty([1,PARAMS().numofBS])
        
        nums1 = np.random.randint(1,PARAMS().length,PARAMS().numofLTEBS)
        nums2 = np.random.randint(1,PARAMS().breadth,PARAMS().numofLTEBS)

        for i in range(0,PARAMS.numofLTEBS):

            b = LTEBaseStation()

            b.bsID = i
            b.x = nums1[i]
            b.y = nums2[i]
            b.pTx = PARAMS().pTxLTE  # Watts

            bss = np.append(bss,b)

        return bss

    # Creates CSVs of locations of BSs and Users

    def createLocationCSV(self, wbss, lbss, luss, wuss):
        wbssl = []
        lbssl = []
        wussl = []
        lussl = []

        # Creating CSVs
        for bs in wbss:
            wbssl.append((bs.x, bs.y))
        wbssdf = pd.DataFrame(wbssl)

        for bs in lbss:
            lbssl.append((bs.x, bs.y))
        lbssdf = pd.DataFrame(lbssl)

        for bs in wuss:
            wussl.append((bs.x, bs.y))
        wussdf = pd.DataFrame(wussl)

        for bs in luss:
            lussl.append((bs.x, bs.y))
        lussdf = pd.DataFrame(lussl)

        wussdf.to_csv("wussdf.csv", index=False)
        lussdf.to_csv("lussdf.csv", index=False)
        wbssdf.to_csv("wbssdf.csv", index=False)
        lbssdf.to_csv("lbssdf.csv", index=False)
        return

    # Returns List of Base Stations of size PARAMS.numofWifiBS
    # each BS with a sequential ID and random location in (length,breadth)
    # If there is one BS then assign static location
    def createWifiBaseStations(self):
        
        bss = np.array([])

        if(PARAMS().numofWifiBS==1):
            b = WifiBaseStation()

            b.bsID = 1
            b.x = (PARAMS().length/2)+10
            b.y = (PARAMS().breadth/2)
            b.pTx = PARAMS().pTxWifi  # Watts

            bss = np.append(bss,b)

            return bss
        
        nums1 = np.random.randint(1,PARAMS().length,PARAMS().numofWifiBS)
        nums2 = np.random.randint(1,PARAMS().breadth,PARAMS().numofWifiBS)

        for i in range(0,PARAMS.numofWifiBS):

            b = WifiBaseStation()

            b.bsID = i
            b.x = nums1[i]
            b.y = nums2[i]
            b.pTx = PARAMS().pTxWifi  # Watts

            bss = np.append(bss,b)

        return bss

    # Returns List of User Equipments of size PARAMS.numofLTEUE
    # each UE with a sequential ID and random location in (length,breadth)
    def createLTEUsers(self):

        uss = np.array([])
        nums1 = np.random.randint(1,PARAMS().length,PARAMS().numofLTEUE)
        nums2 = np.random.randint(1,PARAMS().breadth,PARAMS().numofLTEUE)

        for i in range(0,PARAMS.numofLTEUE):

            u = LTEUserEquipment()

            u.ueID = i
            u.x = nums1[i]
            u.y = nums2[i]

            uss = np.append(uss,u)
        
        return uss

    # Returns List of User Equipments of size PARAMS.numofWifiUE
    # each UE with a sequential ID and random location in (length,breadth)
    def createWifiUsers(self):

        uss = np.array([])
        nums1 = np.random.randint(1,PARAMS().length,PARAMS().numofWifiUE)
        nums2 = np.random.randint(1,PARAMS().breadth,PARAMS().numofWifiUE)

        for i in range(0,PARAMS.numofWifiUE):

            u = WifiUserEquipment()

            u.ueID = i
            u.x = nums1[i]
            u.y = nums2[i]

            uss = np.append(uss,u)
        
        return uss