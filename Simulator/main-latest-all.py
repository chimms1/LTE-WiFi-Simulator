import numpy as np
import pandas as pd
from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass
from running.ServiceClass import GraphService
from running.ConstantParams import PARAMS
from collections import Counter

def count_users(bs_array):
    usercount = 0
    for b in bs_array:
        usercount += len(b.t_user_list)
    
    return usercount


if __name__ == "__main__":
    print("Hello World!")

    # for num in userscenes:
    thisparams = PARAMS()   # this is object of constant params to be used in main

    service = ServiceClass()
    graphservice = GraphService()

    # Scene1: 1 LTE & 1 Wi-Fi (colocated)
    # Scene2: 1 LTE & 1 Wi-Fi (apart)
    # Scene3: 3 LTE & 3  Wi-Fi
    # Scene4: 1 LTE & 3 Wi-Fi
    # Scene5: 3 LTE & 1 Wi-Fi

    # Else choose scene 0 for random allocation of numbers specified in params

    scene = thisparams.scene
    description = "Not Random-Generic"

    print("Scene chosen: ",scene)

    if scene != 0:
        print("Caution: Choosing scene other than 0 will override values set (no. of BS, UE) in PARAMS")

    check = input("Continue? [Y/n]: ")

    if check == 'N' or check == 'n':
        exit()

    # Create BS and UE using Service Class
    lbss = service.createLTEBaseStations(thisparams,scene)
    wbss = service.createWifiBaseStations(thisparams,scene)

    luss = service.createLTEUsers(thisparams)
    wuss = service.createWifiUsers(thisparams)


    # Connecting all the LTE UE with a LTE BS
    i = 0
    for u in luss:
        ind = u.measureSINRandConnect(lbss,wbss)

        # if ind is -1 then that user is out of range of any BS
        if ind == -1:
            luss = np.delete(luss,i)
            continue

        # Add this UE to user_list
        lbss[ind].user_list = np.append(lbss[ind].user_list, u)
        i+=1

    
    # Keeping a copy of LTE transmitting users
    for b in lbss:
        for element in b.user_list:
            b.t_user_list = np.append(b.t_user_list,element)

        b.lusscount = len(b.t_user_list)
        b.lusscount2=b.lusscount

    # Connecting all the Wifi UE with a Wifi BS
    i = 0
    for u in wuss:
        ind = u.measureSNRandConnect(lbss,wbss)
        # if ind is -1 then that user is out of range of any BS
        if ind == -1:
            wuss = np.delete(wuss,i)
            continue

        # Add this UE to user_list
        wbss[ind].user_list = np.append(wbss[ind].user_list, u)
        i+=1
        
    # Keeping a copy of Wifi transmitting users
    for b in wbss:
        for element in b.user_list:
            b.t_user_list = np.append(b.t_user_list,element)

        b.wusscount = len(b.t_user_list)

    # Users decide their data transfer rate
    service.calculate_profile_prob(thisparams)
    print(thisparams.LTE_profile_c_prob)
    print(thisparams.wifi_profile_c_prob)

    service.assign_data_rate_to_users(thisparams, luss, wuss)
    print("LTE data rates")
    for u in luss:        
        print(u.req_data_rate)

    print("wifi data rates")
    for u in wuss:        
        print(u.req_data_rate)
    # exit()
    
    SINR=[]
    SNR=[]

    # Measuring SINR for LTE Users
    for u in luss:
        u.measureSINR(wbss)
        SINR.append(u.SINR)
    
    service.decide_LTE_bits_per_symbol(lbss,thisparams)

    for b in lbss:
        for u in b.user_list:
            print("SINR: ",u.SINR)
            print(b.bits_per_symbol_of_user[u])

    exit()

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
    # for b in luss:
    #     print("{}\t{}\t SINR = {}".format(b.x, b.y, b.SINR))
    print("SINR")
    print(SINR)

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
    format=[[0,1,1,1,1,0,1,1,1,1], # 8:2  9:8       444:01      8:90 
            [0,1,1,1,0,0,1,1,1,0], # 6:4  7:16      333:01      16:90
            [0,1,1,0,0,0,1,1,0,0], # 4:6  4:24      222:01      24:90
            [0,1,1,1,1,0,0,0,0,0], # 4:6  4:24      222:01      24:90
            [0,1,1,1,0,0,0,0,0,0], # 3:7  3:28      166.5:01    28:90        
            [0,1,1,0,0,0,0,0,0,0], # 2:8  2:32      111:01      32:90
            [0,1,1,1,1,0,1,1,1,0]] # 7:3  8:12      388.5:01    12:90

    #============================================================
    # Modifiying for multiple base stations

    formats_required = int(input("Enter the number of formats to simulate[1-7]: "))

    print("\nFormats available:\n")
    for count in range(0,len(format)):
        print("[{}]: {}".format(count,format[count]))

    while 1:
        print("\n-- Choose {} formats from above --".format(formats_required))
        user_formats = list(input("Enter space separated choices => ").split())

        user_formats = [int(x) for x in user_formats]

        print("Formats chosen ",user_formats)

        if len(user_formats) != formats_required:
            print("Expected {} formats... but {} were given".format(formats_required,len(user_formats)))
            continue

        invalid_format = 0
        for num in user_formats:
            if num>6 or num<0:
                print("Invalid format choice...try again")
                invalid_format = 1
                break

        if invalid_format:
            continue
        else:
            break

    print("========================================")

    combos = list(service.my_combinations_with_replacement(user_formats,thisparams.numofLTEBS))

    print("Generated index Combinations: ")
    for combo in combos:
        print(combo)


    print("\nStoring frame structure combinations:")
    chosen_formats = []
    for combo in combos:
        temp_list = []
        for index in combo:
            temp_list.append(format[index])
        chosen_formats.append(temp_list)
    
    for x in chosen_formats:
        print(x)

    print("=============================================================================")
    Fairness = []

    print("LTE users: {} Wifi users: {}".format(count_users(lbss),count_users(wbss)))

    # np.copyto(copy_lbss,lbss)
    # np.copyto(copy_wbss,wbss)
    # copy_lbss = np.array([])
    # copy_wbss = np.array([])

    # for element in lbss:
    #         copy_lbss = np.append(copy_lbss,element)
    # for element in wbss:
    #         copy_wbss = np.append(copy_wbss,element)

    # print("Copy LTE users: {} Wifi users: {}".format(count_users(copy_lbss),count_users(copy_wbss)))

    #Simulation starts
    for simulation_iterator in range(0,len(chosen_formats)):
        # np.copy(lbss,copy_lbss)
        # np.copy(wbss,copy_wbss)
        # lbss = np.array([])
        # wbss = np.array([])
        # for element in copy_lbss:
        #     lbss = np.append(lbss,element)
        # for element in copy_wbss:
        #     wbss = np.append(wbss,element)
        for b in lbss:
            b.lusscount=b.lusscount2
        
        for b in wbss:
            for u in b.user_list:
                u.wifislotsreq = thisparams.wifislotsreq


        for b in wbss:
            b.t_user_list = b.user_list

        print("\n\n-----------------Combination {}---------------------".format(simulation_iterator))

        print(" iter: {} LTE users: {} Wifi users: {}".format(simulation_iterator,count_users(lbss),count_users(wbss)))

        # Select combination
        assigner = 0
        for b in lbss:
            b.format = chosen_formats[simulation_iterator][assigner]
            assigner+=1
        
        # Do work
        LTECountS=0
        LTECountU=0

        WifiCountS=0
        WifiCountU=0

        for slot_iterator in range(0,10):

            single_zero = 0
            multiple_zero = 0
            all_one = 0

            zero_counter = 0
            one_counter = 0

            lbs_single_zero = None

            for b in lbss:
                if b.format[slot_iterator] == 0:
                    zero_counter += 1

                elif b.format[slot_iterator] == 1:
                    one_counter += 1

            if zero_counter > 1:
                multiple_zero=1

            elif zero_counter == 1:
                single_zero=1
                lbs_single_transmission_ind = 0
                for b in lbss:
                    if b.format[slot_iterator]==0:
                        break
                    lbs_single_transmission_ind+=1

                

            elif one_counter == thisparams.numofLTEBS:
                all_one=1

            # "Simulation for one slot in a frame" ==============================
            
    
            # More than one LTE BS has zero
            if multiple_zero == 1:
                LTECountU+=4
                continue
                
            elif single_zero == 1:
                for k in range(0,4):
                    if(lbss[lbs_single_transmission_ind].lusscount>0):
                        LTECountS += 0.5 #0.5 is count not time
                        # print("Hiiiiiiiii")
                        lbss[lbs_single_transmission_ind].lusscount -= 1
                    else:
                        LTECountU += 1

            elif all_one == 1:
                service.assignProb(wbss)

                Wifisensecount = 0
                while Wifisensecount < 111:

                    #Check all prob and count
                    Wifiuserscount,userind = service.countWifiUsersWhoTransmit(wbss)
                    wbs_single_transmission = None
                    wus_single_transmission_ind = None
                    
                    if Wifiuserscount == 1:
                        
                        # Get the only User who is transmitting and its BS
                        bsind = 0
                        for ulist in userind:
                            if len(ulist) == 1:
                                wus_single_transmission_ind = ulist[0]
                                break
                            bsind+=1



                        wbss[bsind].t_user_list[wus_single_transmission_ind].wifislotsreq-=1
                        if wbss[bsind].t_user_list[wus_single_transmission_ind].wifislotsreq == 0:
                            #remwuss = np.delete(remwuss,userind[0])
                            wbss[bsind].t_user_list = np.delete(wbss[bsind].t_user_list,wus_single_transmission_ind)
                        
                        WifiCountS += 1
                        Wifisensecount += 1
                                     
                    else:
                        WifiCountU += 1
                        Wifisensecount += 1

                    service.assignProb(wbss) # assing prob at every "Wifi slot"
                # End of Wifi transmission slot
        # End of slot iteration loop
        # print("\n\n-----------------Combination {}---------------------".format(simulation_iterator))
        print("LTE slots used ",LTECountS," LTE slots unused ",LTECountU)
        print("Wifi slots used ",WifiCountS," Wifi slots unused ",WifiCountU)


        x1=wifirequested=thisparams.wifislotsreq*thisparams.numofWifiUE #x1
        x2=LTErequested=thisparams.LTEslotsreq*thisparams.numofLTEUE #x2

        # print("\nx1",x1,"\nx2",x2,"\ny1",y1,"\ny2",y2,"\n")

        # # Fairness index calculation

        f1=LTECountS/(thisparams.LTEslotsreq*thisparams.numofLTEUE)
        # # f2=WifiCountS/(thisparams.prob*thisparams.numofWifiUE/thisparams.const)
        f2=WifiCountS/(thisparams.wifislotsreq*thisparams.numofWifiUE)
        fair = (f1+f2)**2/(2*((f1)**2+(f2)**2))
        Fairness.append(fair)
        print("Fairness: ",fair)
        # # print("Fairness",Fairness)
        print("-------------------------------------------------------")








    # ground=dict()

    # for k in range(0,len(format)):
    #     d_count = Counter(format[k])
    #     temp_y2= d_count[0]*4 #y2
    #     temp_y1= d_count[1]*111*thisparams.prob #y1 
    #     ground[k]=[temp_y1,temp_y2]
