import numpy as np
import pandas as pd
from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass
from running.ServiceClass import GraphService
from running.ConstantParams import PARAMS
from collections import Counter


if __name__ == "__main__":
    print("Hello World!")

    # Scene1: 1 LTE & 1 Wi-Fi (colocated)
    # Scene2: 1 LTE & 1 Wi-Fi (apart)
    # Scene3: 3 LTE & 3  Wi-Fi
    # Scene4: 1 LTE & 3 Wi-Fi
    # Scene5: 3 LTE & 1 Wi-Fi

    # Else choose scene 0 for random allocation of numbers specified in params

    scene = 1
    description = "Random-Generic"

    print("Scene chosen: ",scene)

    if scene != 0:
        print("Caution: Choosing scene other than 0 will override values set (no. of BS, UE) in PARAMS")

    # for num in userscenes:
    thisparams = PARAMS()
    # thisparams.numofWifiUE = num[0]
    # thisparams.numofLTEUE = num[1]

    service = ServiceClass()
    graphservice = GraphService()
    SINR=[]
    SNR=[]

    # Create BS and UE using Service Class
    lbss = service.createLTEBaseStations(thisparams,scene)
    wbss = service.createWifiBaseStations(thisparams,scene)

    luss = service.createLTEUsers(thisparams)
    wuss = service.createWifiUsers(thisparams)


    # Connecting all the LTE UE with a LTE BS
    for u in luss:
        ind = u.measureSINRandConnect(lbss,wbss)

        # Add this UE to user_list
        lbss[ind].user_list = np.append(lbss[ind].user_list, u)

    # Connecting all the Wifi UE with a Wifi BS
    for u in wuss:
        ind = u.measureSNRandConnect(lbss,wbss)

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
    # print("x\ty of LTE Base Stations")
    # for b in lbss:
    #     print("{}\t{}\t SINR = {}".format(b.x, b.y, b.SINR))

    # print("x\ty of Wifi Base Stations")
    # for b in wbss:
    #     print("{}\t{}\t SNR = {}".format(b.x, b.y, b.SNR))

    print("\nx  y of LTE User Equipments")
    for u in luss:
        print("{}  {}\tLTE-bs: {} SINR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SINR))

    print("\nx  y of Wifi User Equipments")
    for u in wuss:
        print("{}  {}\t Wifi-bs: {} SNR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SNR))

    graphservice.PlotHistSINR(SINR,thisparams)

    graphservice.PlotHistSNR(SNR,thisparams)

    # ====================== Simulation starts here ===============================
    

    # frames=[1,0,1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,1]
    # 1  -->Uplink / s / wifi
    # 0  -->Downlink / LTE
            # '0'/'1' --> SLOT 

    # [0,1,1,1,1,0,1,1,1,1]              wifi:LTE   y2:x2       y1:x1
    format=[[0,1,1,1,1,1,1,1,1,1], # 8:2  9:8       444:01      8:90  
            [0,0,1,1,1,1,1,1,1,1], # 6:4  7:16      333:01      16:90
            [0,0,0,1,1,1,1,1,1,1], # 4:6  4:24      222:01      24:90
            [0,0,0,0,1,1,1,1,1,1], # 4:6  4:24      222:01      24:90
            [0,0,0,0,0,1,1,1,1,1], # 3:7  3:28      166.5:01    28:90        
            [0,0,0,0,0,0,1,1,1,1], # 2:8  2:32      111:01      32:90
            [0,0,0,0,0,0,0,1,1,1]] # 7:3  8:12      388.5:01    12:90

    ground=dict()

    for k in range(0,len(format)):
        d_count = Counter(format[k])
        temp_y2= d_count[0]*4 #y2
        temp_y1= d_count[1]*111*thisparams.prob #y1 
        ground[k]=[temp_y1,temp_y2]
        
        # print(ground[k][0],ground[k][1])
    print(ground)

    Fairness = []
    print("\n\n")
    for i in range(0,len(format)):
        print("Format",i,"\n")
        
        chbusy=0
        # i=6 #Which format to use
        j=0 #Choosesubframe within a format
        curtime=0.0

        service.assignProb(wuss)

        LTECountS=0
        LTECountU=0

        WifiCountS=0
        WifiCountU=0

        remwuss=wuss
        
    
        lusscount=thisparams.numofLTEUE

        while curtime<10000.00:
            if(format[i][j]==0): #LTE will transmit
                for k in range(0,4):
                    if(lusscount>0):
                        chbusy=1
                        curtime += thisparams.subframe/4 
                        LTECountS += 0.5 #0.5 is count not time
                        print("Hiiiiiii")                       
                        lusscount -= 1
                        chbusy=0
                    else:
                        curtime += thisparams.subframe/4 
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
                            curtime += thisparams.wifiuserslot
                            Wifisensecount += 1 
                            chbusy=0                

                        else:
                            curtime += thisparams.wifiuserslot
                            WifiCountU += 1
                            Wifisensecount += 1

                    service.assignProb(remwuss)
                    
                curtime += 1
            j += 1
            # print("Current time after ",j,"th iteration",curtime)
        print("\nLTE slots used ",LTECountS," LTE slots unused ",LTECountU,"remaining LTE users",lusscount)
        print("\nWifi slots used ",WifiCountS," Wifi slots unused ",WifiCountU," remaining wifi users ",remwuss.shape[0])


        x1=wifirequested=thisparams.wifislotsreq*thisparams.numofWifiUE #x1
        x2=LTErequested=thisparams.LTEslotsreq*thisparams.numofLTEUE #x2


        y1=ground[i][0]
        y2=ground[i][1]

        print("\nx1",x1,"\nx2",x2,"\ny1",y1,"\ny2",y2,"\n")

        # Fairness index calculation

        f1=LTECountS/(thisparams.LTEslotsreq*thisparams.numofLTEUE)
        # f2=WifiCountS/(thisparams.prob*thisparams.numofWifiUE/thisparams.const)
        f2=WifiCountS/(thisparams.numofWifiUE*thisparams.const)
        Fairness.append((f1+f2)**2/(2*((f1)**2+(f2)**2)))
        print("Fairness",Fairness[i])
        # print("Fairness",Fairness)
        print("-------------------------------------------------------")
    # End of for loop


    for i in range(0,len(format)):
        print("Frame: ",i,"Fairness: ",Fairness[i])

    # 11-12-22
    # minimize x1 x2 y1 and y2

    loss=[]
    for i in range(0,len(format)):

        loss.append(WifiCountS/x1-LTECountS/x2)
        
    # csvlist.append((thisparams.numofWifiUE,thisparams.numofLTEUE,max(Fairness),Fairness.index(max(Fairness))))

# csvframe = pd.DataFrame(csvlist)
# csvframe.to_csv("csvframe.csv", index=False)

    # Plot Fairness vs Frame Format graph
    import matplotlib.pyplot as plt
    # plt.bar([p for p in range(0,7)], Fairness)
    # plt.title('Fairness vs Frame Format for {} LTEUE {} WIFI UE'.format(thisparams.numofLTEUE,thisparams.numofWifiUE), fontsize=18)
    # plt.xlabel('Frame Format', fontsize=18)
    # plt.ylabel('Fairness', fontsize=18)
    # plt.ylim([0.5,0.6])
    # plt.xticks(fontsize=12)
    # plt.yticks(fontsize=12)
    # # plt.yticks(ticks=True)
    # plt.show()

    # 2,2; 4,4; 6,6
    # 2,6; 6,2; 10,10

    # xlabels = ["2,2","4,4","6,6","2,6","6,2","10,10"]
    # xt = [0,1,2,3,4,5]

    
    # plt.plot([1.0,0.9392346461720907,0.6414923207159269,0.6587471270511519,1.0,0.5111097395383285])
    # plt.title("Fairness vs No. of Users for Format 0",fontsize=17)
    # plt.xlabel("(LTE,Wifi) Users",fontsize=17)
    # plt.ylabel("Fairness",fontsize=17)
    # plt.xticks(xt,xlabels,fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()

    # plt.plot([0.9210720913531615,0.8482732115879031,0.6274873524451938,0.6133209677637724,0.9196927325110418,0.5044443566546833])
    # plt.title("Fairness vs No. of Users for Format 1",fontsize=17)
    # plt.xlabel("(LTE,Wifi) Users",fontsize=17)
    # plt.ylabel("Fairness",fontsize=17)
    # plt.xticks(xt,xlabels,fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()

    # plt.plot([0.9853458382180539,0.7999999999999999,0.5754907409617398,0.5553846153846154,0.9909664180971924,0.5066663703835385])
    # plt.title("Fairness vs No. of Users for Format 2",fontsize=17)
    # plt.xlabel("(LTE,Wifi) Users",fontsize=17)
    # plt.ylabel("Fairness",fontsize=17)
    # plt.xticks(xt,xlabels,fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()

    # plt.plot([0.9900990099009901,0.7444450865381836,0.5663716814159292,0.5791278893436339,0.9858500017680132,0.5044443566546833])
    # plt.title("Fairness vs No. of Users for Format 3",fontsize=17)
    # plt.xlabel("(LTE,Wifi) Users",fontsize=17)
    # plt.ylabel("Fairness",fontsize=17)
    # plt.xticks(xt,xlabels,fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()

    # plt.plot([0.9987867736794495,0.6923076923076923,0.559051889113675,0.5351416798819021,0.9981132075471698,0.5044443566546833])
    # plt.title("Fairness vs No. of Users for Format 4",fontsize=17)
    # plt.xlabel("(LTE,Wifi) Users",fontsize=17)
    # plt.ylabel("Fairness",fontsize=17)
    # plt.xticks(xt,xlabels,fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()

    # plt.plot([0.9520222045995241,0.638879433589761,0.5332963374028857,0.5480367871463958,0.9392346461720907,0.5022222112483394])
    # plt.title("Fairness vs No. of Users for Format 5",fontsize=17)
    # plt.xlabel("(LTE,Wifi) Users",fontsize=17)
    # plt.ylabel("Fairness",fontsize=17)
    # plt.xticks(xt,xlabels,fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()

    # plt.plot([0.8736005507217872,0.9234017529447226,0.6484292246014401,0.6327590097295989,0.8849482659459822,0.5077773072986944])
    # plt.title("Fairness vs No. of Users for Format 6",fontsize=17)
    # plt.xlabel("(LTE,Wifi) Users",fontsize=17)
    # plt.ylabel("Fairness",fontsize=17)
    # plt.xticks(xt,xlabels,fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.show()



        # userscenes =   [[1,1],
    #                 [1,2],
    #                 [1,3],
    #                 [1,4],  
    #                 [1,6],   
    #                 [1,8],     
    #                 [1,16],    
    #                 [1,24],    
    #                 [1,32],
    #                 [2,1],
    #                 [2,2], 
    #                 [2,3], 
    #                 [2,4], 
    #                 [2,6], 
    #                 [2,8], 
    #                 [2,16],
    #                 [2,24],
    #                 [2,32],
    #                 [3,1], 
    #                 [3,2], 
    #                 [3,3], 
    #                 [3,4], 
    #                 [3,6], 
    #                 [3,8], 
    #                 [3,16],
    #                 [3,24],
    #                 [3,32],
    #                 [4,1], 
    #                 [4,2], 
    #                 [4,3], 
    #                 [4,4], 
    #                 [4,6],
    #                 [4,8], 
    #                 [4,16],
    #                 [4,24],
    #                 [4,32],
    #                 [6,1], 
    #                 [6,2], 
    #                 [6,3], 
    #                 [6,4], 
    #                 [6,6], 
    #                 [6,8], 
    #                 [6,16],
    #                 [6,24],
    #                 [6,32],
    #                 [8,1],
    #                 [8,2],
    #                 [8,3],
    #                 [8,4],
    #                 [8,6],
    #                 [8,8],
    #                 [8,16],
    #                 [8,24],
    #                 [8,32]]

    # csvlist = []
    # csvlist.append(("x","y","fairness","format"))

    # thisparams0 = PARAMS()