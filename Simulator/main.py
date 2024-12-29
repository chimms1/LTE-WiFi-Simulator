import numpy as np
import time
from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass
from running.ServiceClass import GraphService
from running.ConstantParams import PARAMS
from collections import Counter


if __name__ == "__main__":
    print("Hello World!")

    service = ServiceClass()
    graphservice = GraphService()
    SINR=[]
    SNR=[]

    scene = 2
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

    #  Simulation starts here
    


    # frames=[1,0,1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,1]
    # 1  -->Uplink / s / wifi
    # 0  -->Download / LTE

    chbusy=0
    i=6 #Which format to use
    j=0 #Choosesubframe within a format
    curtime=0.0
    # [0,1,1,1,1,0,1,1,1,1] '0'/'1' --> SLOT        q2:p2        q1:p1
    format=[[0,1,1,1,1,1,1,1,1,1], # 8:2  9:8       444:01      8:90  
            [0,0,1,1,1,1,1,1,1,1], # 6:4  7:16      333:01      16:90
            [0,0,0,1,1,1,1,1,1,1], # 4:6  4:24      222:01      24:90
            [0,0,0,0,1,1,1,1,1,1], # 4:6  4:24      222:01      24:90
            [0,0,0,0,0,1,1,1,1,1], # 3:7  3:28      166.5:01    28:90        
            [0,0,0,0,0,0,1,1,1,1], # 2:8  2:32      111:01      32:90
            [0,0,0,0,0,0,0,1,1,1]] # 7:3  8:12      388.5:01    12:90


    ground=dict()

    service.assignProb(wuss)

    LTECountS=0
    LTECountU=0

    WifiCountS=0
    WifiCountU=0

    remwuss=wuss
    
    lusscount=PARAMS().numofLTEUE

    while curtime<10000.00:

        if(format[i][j]==0): #LTE will transmit
            for k in range(0,4):
                if(lusscount>0):
                    chbusy=1
                    curtime += PARAMS().subframe/4 
                    LTECountS += 0.5 #0.5 is count not time
                    lusscount -= 1
                    chbusy=0
                else:
                    curtime += PARAMS().subframe/4 
                    LTECountU += 1

        if(format[i][j]==1): #LTE will transmit
            Wifisensecount=0
            while Wifisensecount < 111:  
                if(chbusy==0):
                    #Check all prob and count 
                    Wifiuserscount,userind = service.countWifiUsersWhoTransmit(remwuss)

                    if Wifiuserscount == 1:
                        remwuss[userind[0]].wifislotsreq-=1
                        if remwuss[userind[0]].wifislotsreq==0:
                            remwuss = np.delete(remwuss,userind[0])
                        chbusy=1                
                        WifiCountS += 1
                        curtime += PARAMS().wifiuserslot
                        Wifisensecount += 1 
                        chbusy=0                

                    else:
                        curtime += PARAMS().wifiuserslot
                        WifiCountU += 1
                        Wifisensecount += 1

                service.assignProb(remwuss)
                
            curtime += 1
        j += 1
        print("Current time after ",j,"th iteration",curtime)
    print("\nLTE slots used ",LTECountS," LTE slots unused ",LTECountU)
    print("\nWifi slots used ",WifiCountS," Wifi slots unused ",WifiCountU," remaining wifi users ",remwuss.shape[0])

    p1=wifineeded=PARAMS.wifislotsreq*PARAMS.numofWifiUE #x1
    p2=LTEneeded=PARAMS.LTEslotsreq*PARAMS.numofLTEUE #x2


    for k in range(0,len(format)):
        d_count = Counter(format[k])
        temp_q1= d_count[0]*4 #y2
        temp_q2= d_count[1]*111*PARAMS().prob #y1 
        ground[k]=[temp_q1,temp_q2]
        
        # print(ground[k][0],ground[k][1])
   
    q1=ground[i][0]
    q2=ground[i][1]
    

    # x1==y1
    # x2==y2

    print("\np1",p1,"\np2",p2,"\nq1",q1,"\nq2",q2,"\n")

    # Fairness index calculation

    x1=LTECountS/(PARAMS.LTEslotsreq*PARAMS.numofLTEUE)
    # x2=WifiCountS/(PARAMS.prob*PARAMS.numofWifiUE/PARAMS.const)
    x2=WifiCountS/(PARAMS.numofWifiUE*PARAMS.const)
    print(x1,x2)
    Fairness=(x1+x2)**2/(2*((x1)**2+(x2)**2))
    print("Fairness",Fairness)

    # 11-12-22 
    # minimize p1 p2 q1 and q2
    # multiple wifi and LTE bs