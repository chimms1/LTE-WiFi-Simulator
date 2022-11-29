import numpy as np
import time
from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass
from running.ServiceClass import GraphService
from running.ConstantParams import PARAMS


if __name__ == "__main__":
    print("Hello World!")

    service = ServiceClass()
    graphservice = GraphService()
    SINR=[]
    SNR=[]

    scene = 1
    description = "single"

    # Scene1: 1 LTE & 1 Wi-Fi (colocated)
    # Scene2: 1 LTE & 1 Wi-Fi (apart)
    # Scene3: 3 LTE & 3  Wi-Fi
    # Scene4: 1 LTE & 3 Wi-Fi
    # Scene5: 3 LTE & 1 Wi-Fi


    # Create BS and UE using Service Class
    lbss = service.createLTEBaseStations(scene)
    wbss = service.createWifiBaseStations(scene)

    luss = service.createLTEUsers()
    wuss = service.createWifiUsers()


    # Connecting all the LTE UE with a LTE BS
    for u in luss:
        ind = u.measurePowerRcvd(lbss)

        # Add this UE to user_list
        lbss[ind].user_list = np.append(lbss[ind].user_list, u)

    # Connecting all the Wifi UE with a Wifi BS
    for u in wuss:
        ind = u.measurePowerRcvd(wbss)
        print("\nINDEX:", ind)

        # Add this UE to user_list
        wbss[ind].user_list = np.append(wbss[ind].user_list, u)


    # Measuring SINR for LTE Users
    for u in luss:
        u.measureSINR(wbss)
        SINR.append(u.SINR)

    # Measuring SNR for Wifi Users
    for u in wuss:
        u.measureSNR()
        SNR.append(u.SNR)

    # Creating CSVs
    service.createLocationCSV(wbss, lbss, luss, wuss)

    # Plotting Graphs for scenes
    graphservice.PlotScene(scene, description)


    # Printing
    print("x\ty of LTE Base Stations")
    for b in lbss:
        print("{}\t{}\t SINR = {}".format(b.x, b.y, b.SINR))

    print("x\ty of Wifi Base Stations")
    for b in wbss:
        print("{}\t{}\t SNR = {}".format(b.x, b.y, b.SNR))

    print("\n\n")

    print("\n\n\nx\ty of LTE User Equipments\n")
    for u in luss:
        print("{}\t{}\tLTE-bs: {} SINR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SINR))

    print("\n\n\nx\ty of Wifi User Equipments\n")
    for u in wuss:
        print("{}\t{}\t Wifi-bs: {} SNR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SNR))

    # print("tttttttttttttttttttttttttttttttttttttttttt\n\n")
    graphservice.PlotHistSINR(SINR)
    # graphservice.PlotHistSINR(SINR)
   
    graphservice.PlotHistSNR(SNR)
    # graphservice.PlotHistSNR(SNR)

    

    service.assignProb(wuss)


    # Probabilities
    for u in wuss:
        print(u.probability)

    LTECountS=0
    LTECountU=0

    WifiCountS=0
    WifiCountU=0



    # frames=[1,0,1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,1]
    # 1  -->Uplink / s / wifi
    # 0  -->Download / LTE


    chbusy=0
    i=0 #Which format to use
    j=0 #Choosesubframe within a format
    curtime=0.0
    # [0,1,1,1,1,0,1,1,1,1]
    format=[[0,1,1,1,1,1,1,0,0,0],[0,1,1,1,0,0,1,1,1,0],[0,1,1,0,0,0,1,1,0,0],[0,1,1,1,1,0,0,0,0,0],[0,1,1,1,0,0,0,0,0,0],[0,1,1,0,0,0,0,0,0,0],[0,1,1,1,1,0,1,1,1,0]]
    lusscount=PARAMS().numofLTEUE
    while curtime<10000.00:

        if(format[i][j]==0): #LTE will transmit
            for k in range(0,4):
                if(lusscount>0):
                    chbusy=1
                    curtime += 250 
                    LTECountS += 1
                    lusscount -= 1
                    chbusy=0
                else:
                    curtime += 250 
                    LTECountU += 1

        if(format[i][j]==1): #LTE will transmit
            Wifisensecount=0
            while Wifisensecount < 111:
                if(chbusy==0):
                    #Check all prob and count
                    Wifiuserscount=service.countWifiUsersWhoTransmit(wuss)

                    if Wifiuserscount == 1:
                        chbusy=1                
                        WifiCountS += 1
                        curtime += 9
                        Wifisensecount += 1
                        chbusy=0                

                    else:
                        curtime += 9
                        WifiCountU += 1
                        Wifisensecount += 1

                service.assignProb(wuss)
                
            curtime += 1
        j += 1
        print("Current time at ",j,"th iteration",curtime)
    print("LTE slots used ",LTECountS," LTE slots unused ",LTECountU)
    print("Wifi slots used ",WifiCountS," Wifi slots unused ",WifiCountU)


    # Fairness index calculation

    x1=LTECountS/(0.5*PARAMS.numofLTEUE)
    x2=WifiCountS/(PARAMS.prob*PARAMS.numofWifiUE/PARAMS.const)
    Fairness=(x1+x2)**2/(2*((x1)**2+(x2)**2))
    print(Fairness)







            

            
        

