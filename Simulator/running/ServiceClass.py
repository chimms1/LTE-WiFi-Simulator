import random
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from running.ConstantParams import PARAMS
from entities.BaseStation import LTEBaseStation
from entities.BaseStation import WifiBaseStation
from entities.UserEquipment import LTEUserEquipment
from entities.UserEquipment import WifiUserEquipment

class ServiceClass:



    
    def countWifiUsersWhoTransmit(self,wuss):
        WifiUsersWhoTransmit=0
        for u in wuss:
            if u.probability<PARAMS.prob:
                WifiUsersWhoTransmit += 1
            return WifiUsersWhoTransmit 






    # Returns List of Base Stations of size PARAMS.numofLTEBS
    # each BS with a sequential ID and random location in (length,breadth)
    # Locations are assigned based on scenes
    def createLTEBaseStations(self,scenenum=1):
        
        bss = np.array([])

        if(scenenum == 1):
            b = LTEBaseStation()

            b.bsID = 0
            b.x = PARAMS().length/2
            b.y = PARAMS().breadth/2
            b.pTx = PARAMS().pTxLTE  # Watts

            bss = np.append(bss,b)

            return bss

        elif(scenenum == 2):
            b = LTEBaseStation()

            b.bsID = 0
            b.x = 35
            b.y = 50
            b.pTx = PARAMS().pTxLTE  # Watts

            bss = np.append(bss,b)

            return bss

        elif(scenenum == 3):
            scene_params = PARAMS()

            scene_params.numofLTEBS = 5

            nums1 = np.random.randint(30,70,scene_params.numofLTEBS)
            nums2 = np.random.randint(30,70,scene_params.numofLTEBS)
            
            for i in range(0,scene_params.numofLTEBS):

                b = LTEBaseStation()

                b.bsID = i
                b.x = nums1[i]
                b.y = nums2[i]
                b.pTx = scene_params.pTxLTE  # Watts

                bss = np.append(bss,b)

            return bss

        elif(scenenum == 4):

            nums1 = np.random.randint(40,60,1)
            nums2 = np.random.randint(40,60,1)

            b = LTEBaseStation()

            b.bsID = 0
            b.x = nums1[0]
            b.y = nums2[0]
            b.pTx = PARAMS().pTxLTE  # Watts

            bss = np.append(bss,b)

            return bss

        elif(scenenum == 5):
            scene_params = PARAMS()

            scene_params.numofLTEBS = 5

            nums1 = np.random.randint(30,70,scene_params.numofLTEBS)
            nums2 = np.random.randint(30,70,scene_params.numofLTEBS)
            
            for i in range(0,scene_params.numofLTEBS):

                b = LTEBaseStation()

                b.bsID = i
                b.x = nums1[i]
                b.y = nums2[i]
                b.pTx = scene_params.pTxLTE  # Watts

                bss = np.append(bss,b)

            return bss

        
        #------------------------- Generic Scene ----------------
        elif(scenenum == 0):
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

    # Returns List of Base Stations of size PARAMS.numofWifiBS
    # each BS with a sequential ID and random location in (length,breadth)
    # If there is one BS then assign static location
    def createWifiBaseStations(self,scenenum=1):
        
        bss = np.array([])

        if(scenenum==1):
            b = WifiBaseStation()

            b.bsID = 0
            b.x = (PARAMS().length/2)+10
            b.y = (PARAMS().breadth/2)
            b.pTx = PARAMS().pTxWifi  # Watts

            bss = np.append(bss,b)

            return bss

        elif(scenenum==2):
            b = WifiBaseStation()

            b.bsID = 0
            b.x = 65
            b.y = 50
            b.pTx = PARAMS().pTxWifi  # Watts

            bss = np.append(bss,b)

            return bss

        elif (scenenum==3):
            
            scene_params = PARAMS()

            scene_params.numofWifiBS = 5

            nums1 = np.random.randint(30,70,scene_params.numofWifiBS)
            nums2 = np.random.randint(30,70,scene_params.numofWifiBS)

            for i in range(0,scene_params.numofWifiBS):

                b = WifiBaseStation()

                b.bsID = i
                b.x = nums1[i]
                b.y = nums2[i]
                b.pTx = scene_params.pTxWifi  # Watts

                bss = np.append(bss,b)

            return bss

        elif (scenenum==4):
            
            scene_params = PARAMS()

            scene_params.numofWifiBS = 5

            nums1 = np.random.randint(30,70,scene_params.numofWifiBS)
            nums2 = np.random.randint(30,70,scene_params.numofWifiBS)

            for i in range(0,scene_params.numofWifiBS):

                b = WifiBaseStation()

                b.bsID = i
                b.x = nums1[i]
                b.y = nums2[i]
                b.pTx = scene_params.pTxWifi  # Watts

                bss = np.append(bss,b)

            return bss

        elif(scenenum==5):
            b = WifiBaseStation()

            num1 = np.random.randint(40,60,1)
            num2 = np.random.randint(40,60,1)

            b.bsID = 0
            b.x = num1[0]
            b.y = num2[0]
            b.pTx = PARAMS().pTxWifi  # Watts

            bss = np.append(bss,b)

            return bss

        
        
        #-----------------------Generic Scene----------------------------
        elif (scenenum==0):
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
    

    # Assigning random number to each user
    def assignProb(self,wuss):
        for u in wuss:
            u.probability=round(random.uniform(0,1),4) #Assigning random number to each user







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

class GraphService:
    
    # Plot coordinates Scatter plot for given Scenario
    def PlotScene(self,scenenum,description):

        wussdf = pd.read_csv("wussdf.csv")
        lussdf = pd.read_csv("lussdf.csv")
        wbssdf = pd.read_csv("wbssdf.csv")
        lbssdf = pd.read_csv("lbssdf.csv")

        x1 = lussdf.iloc[:, 0:1]
        y1 = lussdf.iloc[:, 1:2]

        x2 = wussdf.iloc[:, 0:1]
        y2 = wussdf.iloc[:, 1:2]

        x3 = lbssdf.iloc[:, 0:1]
        y3 = lbssdf.iloc[:, 1:2]

        x4 = wbssdf.iloc[:, 0:1]
        y4 = wbssdf.iloc[:, 1:2]

        plt.scatter(x1, y1, marker='x', color='red')
        plt.scatter(x2, y2, marker='x', color='blue')
        plt.scatter(x3, y3, marker='^', color='red', s=100)
        plt.scatter(x4, y4, marker='^', color='blue', s=100)
        plt.legend(["LTE User", "Wi-Fi User", "LTE BS", "Wi-Fi BS"])
        plt.xlim(0, 100)
        plt.ylim(0, 100)

        plt.xlabel("X-Coordinates")
        plt.ylabel("Y-Coordinates")
        plt.title("Scene{} : {} LTE BS & {} Wi-Fi BS, {}".format(scenenum,PARAMS().numofLTEBS,PARAMS().numofWifiBS,description))

        plt.show()

    def PlotHistSINR(self,SINR):

        maxind=0
        minind=0
        maxSINR=max(SINR)
        minSINR=min(SINR)
        print("SINR:MIN = {}, MAX = {}".format(minSINR,maxSINR))
        # for i in range(1,len(SINR)):
        #     if(SINR[i]>maxSINR):
        #         maxSINR=SINR[i]
        #         maxind=i
        # if (SINR[i] < minSINR):
        #     minSINR = SINR[i]
        #     minind = i

        plt.hist(SINR,label="SINR of LTE Users", bins=5, edgecolor="black")
        plt.title("SINR of LTE Users")
        plt.ylabel("No. of LTE Users")
        plt.xlabel("SINR")
        plt.show()

    def PlotHistSNR(self,SNR):

        maxind=0
        minind=0
        maxSNR=max(SNR)
        minSNR=min(SNR)
        print("SNR:MIN = {}, MAX = {}".format(minSNR,maxSNR))
        # for i in range(1,len(SINR)):
        #     if(SINR[i]>maxSINR):
        #         maxSINR=SINR[i]
        #         maxind=i
        # if (SINR[i] < minSINR):
        #     minSINR = SINR[i]
        #     minind = i

        plt.hist(SNR,label="SNR of Wi-Fi Users", bins=5, edgecolor="black")
        plt.title("SNR of Wi-Fi Users")
        plt.ylabel("No. of Wi-Fi Users")
        plt.xlabel("SNR")
        plt.show()



        

