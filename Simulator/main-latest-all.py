import numpy as np
import pandas as pd
from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass
from running.ServiceClass import GraphService
from running.Print import Verbose
from collections import Counter
from entities.UserEquipment import WifiUserEquipment
import copy

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
    verbose = Verbose()

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

    if verbose.profile_and_probability == 1:
        print("\n=== Profile and Probability Info ===")
        print("DataRate Profiles: ",thisparams.profiles)
        print("LTE user ratio:    ",thisparams.LTE_ratios)
        print("Wifi user ratio:   ",thisparams.wifi_ratios)
        print("\nLTE Prob: ",thisparams.LTE_profile_prob)
        print("LTE Cumulative Prob: ",thisparams.LTE_profile_c_prob)
        print("\nWifi Prob: ",thisparams.wifi_profile_prob)
        print("Wifi Cumulative Prob: ",thisparams.wifi_profile_c_prob)
        print("======")

    # Based on ratios decided by the user, assign data rates to UE
    service.assign_data_rate_to_users(thisparams, luss, wuss)

    if verbose.LTE_user_data_rates == 1:
        print("\n=== LTE user required data rates ===")
        for u in luss:        
            print("LTE userid {}: {} Kbps".format(u.ueID,u.req_data_rate))
        print("======")
        

    if verbose.Wifi_user_data_rates == 1:
        print("\n=== Wifi user required data rates ===")
        for u in wuss:        
            print("Wifi userid {}: {} Kbps".format(u.ueID,u.req_data_rate))
        print("======")
    # exit()
    
    SINR=[]
    SNR=[]
    
    #
    # Measuring SINR for LTE Users
    for u in luss:
        u.measureSINR(wbss)
        SINR.append(u.SINR)

    service.decide_LTE_bits_per_symbol(lbss,thisparams)

    service.calculate_LTE_user_PRB(thisparams, luss)

    if verbose.LTE_user_SINR_MCS_value == 1:
        print("\n=== LTE user SINR and MCS value ===")
        for b in lbss:
            for u in b.user_list:
                print("LTE userid {}: {:.4f} @> {} bits per symbol".format(u.ueID,u.SINR,b.bits_per_symbol_of_user[u]))
                if verbose.LTE_user_req_PRB == 1:
                    print("Required PRBs: {}".format(u.req_no_PRB))
        print("======")

    #
    # Measuring SNR for Wifi Users
    for u in wuss:
        u.measureSNR()
        SNR.append(u.SNR)

    service.decide_wifi_bits_per_symbol(wbss, thisparams)

    service.calculate_wifi_user_slots(thisparams, wuss)

    if verbose.Wifi_user_SNR_MCS_value == 1:
        print("\n=== Wifi user SNR and MCS value ===")
        for b in wbss:
            for u in b.user_list:
                print("Wifi userid {}: {:.4f} @> {} Mbps".format(u.ueID,u.SNR,b.bits_per_symbol_of_user[u]))
                if verbose.Wifi_user_req_slots == 1:
                    print("Required wifi slots: {}".format(u.req_no_wifi_slot))
        print("======")

    

    
    if verbose.plot_Scene == 1:
        # Creating CSVs
        service.createLocationCSV(wbss, lbss, luss, wuss)

        # Plotting Graphs for scenes
        graphservice.PlotScene(scene, description)

    # print("\nx  y of LTE User Equipments")
    # for u in luss:
    #     print("{}  {}\tLTE-bs: {} SINR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SINR))

    # print("\nx  y of Wifi User Equipments")
    # for u in wuss:
    #     print("{}  {}\t Wifi-bs: {} SNR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SNR))

    if verbose.plot_SINR_Count == 1:
        graphservice.PlotHistSINR(SINR,thisparams)
    if verbose.plot_SNR_Count == 1:
        graphservice.PlotHistSNR(SNR,thisparams)

    # ====================== Simulation starts here ===============================
    # frames=[1,0,1,0,1,0,0,0,1,1,0,1,0,1,0,1,1,1]
    # 1  -->Uplink / s / wifi
    # 0  -->Downlink / LTE
            # '0'/'1' --> SLOT 

    # [0,1,1,1,1,0,1,1,1,1]              wifi:LTE   y2:x2       y1:x1
    format=[[0,1,0,1,1,0,1,1,1,1], # 8:2  9:8       444:01      8:90 
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
    # exit()

    #Simulation starts
    for simulation_iterator in range(0,len(chosen_formats)):


        for b in lbss:
            b.lusscount=b.lusscount2
        
        # for b in wbss:
        #     for u in b.user_list:
        #         u.wifislotsreq = thisparams.wifislotsreq


        for b in wbss:
            b.t_user_list = b.user_list
        
        allwuss = []

        for u in wuss:
            # tempu = WifiUserEquipment()
            tempu = copy.copy(u)

            allwuss.append(tempu)
        # for u in wuss:
        #     twuss.append(u)
        # # twuss = wuss

        # service.calculate_wifi_user_slots(thisparams, wuss)

        # twuss[0].random_backoff_slots = 69

        # print(twuss[0].random_backoff_slots)
        # print(wuss[0].random_backoff_slots)

        

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

        channel_busy = 0

        CTS = 0
        tuserlist = []
        RTSuserlist = []

        for slot_iterator in range(0,2):

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

            # More than one LTE BS has zero
            if multiple_zero == 1 or single_zero == 1:
                channel_busy = 1
            elif all_one == 1:
                channel_busy = 0

            # "Simulation for one sub-frame (0/1) in a frame" ==============================
            # service.assignProb2(allwuss)

            Wifisensecount = 0
            rem_wifi_slots=111
            
            while Wifisensecount < 111:
                print("current wifi slot ", Wifisensecount)
                if len(allwuss) == 0 and len(tuserlist)!=0 and channel_busy==1:
                    print("All the remaining {} Wifi users are waiting".format(len(tuserlist)))
                    # do not break
                if len(allwuss)==0 and len(tuserlist)==0 and RTSuserlist ==0:
                    print("All wifi users have finished transmitting and are not programmed to do it again in this simulation")
                    break   # break here

                # step1:
            # set rem_wifi_slots=111
            # if CTS!=0
                # if(CTS > rem_wifi_slots)
                    # And current wifi user's remaining slots!=0
                        # Wifi failed
                        # make CTS=0 (????????)
                    # And current wifi user's remaining slots==0
                        # Wifi success
                # else
                    # Allocate slots to wifi user
                    # and decrement CTS
                    # and decrement rem_wifi_slots
                if CTS!=0:
                    print("tuserlist ",[(u.ueID) for u in tuserlist])
                    print("current status of random backoff ", [(u.ueID,u.random_backoff_slots) for u in tuserlist if u.random_backoff_flag==1])
                    print("current status of DIFS ", [(u.ueID,u.DIFS_slots) for u in tuserlist if u.DIFS_flag==1])

                    for u in tuserlist:
                            if u.random_backoff_flag == 1 and u.random_backoff_slots > 0:
                                u.random_backoff_slots-=1
                                # Random backoff of this user become zero and now channel is busy so set randombackoff again
                            if u.random_backoff_flag == 1 and u.random_backoff_slots == 0:
                                u.setRandomBackoff()

                    if channel_busy == 1:

                        print("current status of tuserlist ", [(u.ueID,u.DIFS_slots) for u in tuserlist])
                        print("\n")
                        print(" Wifi user ",selected_user.ueID," used 1 slot during LTE's period")

                        WifiCountU+=1

                    
                    if channel_busy == 0:
                        selected_user.req_no_wifi_slot-=1
                        WifiCountS+=1
                        # print(Wifisensecount," Success ",[(u.ueID,u.DIFS_slots) for u in tuserlist])
                        print(" Wifi user ",selected_user.ueID," used 1 slot successfully")

                    CTS-=1
                    # When CTS becomes zero
                    if CTS==0 and channel_busy==1:
                        print("User ",selected_user.ueID, "was till now sending during period 0 and is added back to allwuss")
                        print("\n")
                        allwuss.append(selected_user)

                        print("current status of allwuss ",[u.ueID for u in allwuss])
                        
                    
                    if CTS==0 and channel_busy==0:
                        if selected_user.req_no_wifi_slot == 0:
                            print("User ",selected_user.ueID, "has completed his transmission compleetly and is added back to allwuss")
                            
                            selected_user.req_no_wifi_slot=t_req_no_wifi_slot
                            allwuss.append(selected_user)
                            print("current status of allwuss ",[u.ueID for u in allwuss])

                        elif selected_user.req_no_wifi_slot > 0:
                            allwuss.append(selected_user)


            #else if CTS==0
                if CTS == 0:
                    print("current status of random backoff", [(u.ueID,u.random_backoff_slots) for u in tuserlist if u.random_backoff_flag==1])
                    print("current status of DIFS", [(u.ueID,u.DIFS_slots) for u in tuserlist if u.DIFS_flag==1])

                    service.assignProb2(allwuss)

                    # For all users in the list(list of users with prob<threshold)
                    Wifiuserscount,a = service.countWifiUsersWhoTransmit2(allwuss)
                    print("New Users who want to transmit: ",[x.ueID for x in a])
                    # if channel is busy
                    if channel_busy == 1:
                        # print("current status of random backoff", [(u.ueID,u.random_backoff_slots) for u in tuserlist])
                        WifiCountU +=1
                        for u in a:
                            if u.random_backoff_flag == 0 and u.random_backoff_slots == 0:
                                u.random_backoff_flag = 1
                                u.setRandomBackoff()
                           
                        for u in tuserlist:
                            if u.random_backoff_flag == 1 and u.random_backoff_slots > 0:
                                u.random_backoff_slots-=1
                            if u.random_backoff_flag == 1 and u.random_backoff_slots == 0:
                                u.random_backoff_flag = 1
                                u.setRandomBackoff()
                            if u.random_backoff_flag == 0 and u.random_backoff_slots == 0:
                                u.random_backoff_flag = 1
                                u.setRandomBackoff()
            
                    for u in a:
                        tuserlist.append(u)
                        allwuss.remove(u)
                        

                    # if channel is free
                    if channel_busy == 0:
                        # print("current status of random backoff", [(u.ueID,u.random_backoff_slots) for u in tuserlist])


                        for u in tuserlist:
                            if u.random_backoff_flag == 1 and u.random_backoff_slots > 0:
                                u.random_backoff_slots-=1

                            # if random
                            if u.random_backoff_slots == 0 and u.DIFS_flag == 0:
                                u.random_backoff_flag = 0
                                u.DIFS_flag = 1
                                u.DIFS_slots = thisparams.DIFS_slots
                                #Decrement DIFS or not7

                            if u.random_backoff_flag == 0 and u.DIFS_flag == 1:
                                if u.DIFS_slots > 0:
                                    u.DIFS_slots -=1
                                
                                if u.DIFS_slots == 0:
                                    u.DIFS_flag = 0
                                    u.DIFS_slots = thisparams.DIFS_slots
                                    # send RTS
                                    RTSuserlist.append(u)
                        
                        if len(RTSuserlist)>0:
                            selected_user = service.sendRTS(thisparams,RTSuserlist)
                            RTSuserlist.remove(selected_user)
                            tuserlist.remove(selected_user)
                            print("Selected userid: {} ".format(selected_user.ueID))
                            CTS = selected_user.req_no_wifi_slot
                            t_req_no_wifi_slot=selected_user.req_no_wifi_slot
                        else:
                            WifiCountU+=1

                            # if CTS>rem_wifi_slots:
                            #     WifiCountU = CTS-rem_wifi_slots

                    # <check for empty slot here>
                # print(Wifisensecount)
                Wifisensecount+=1
                rem_wifi_slots-=1
            # End of while 111
            print("\nWifi Successful: ",WifiCountS," Wifi Unused: ",WifiCountU,"\n")


                    # sense channel

                # if channel_busy == 1:
                    # start random backoff algorithm and start countdown
                # else
                    # start DIFS
                        # untill DIFS==0
                            # sense channel  
                                # if busy 
                                    # dont decrement
                                # else 
                                    # decrement
                                        # and DIFS==0 
                                            # send RTS to wifi
                                                # if wifi has multiple RTS
                                                    # choose a user and broadcast CTS
                                                # else
                                                    # choose the only user present 
                                                # wifi broadcasts CTS to list of wifi users
                                                # untill CTS ends no one sends request
                                                # CTS ends goto step1




    
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

            # exit()
        # End of slot iteration loop
        # print("\n\n-----------------Combination {}---------------------".format(simulation_iterator))
        # print("LTE slots used ",LTECountS," LTE slots unused ",LTECountU)
        # print("Wifi slots used ",WifiCountS," Wifi slots unused ",WifiCountU)


        # x1=wifirequested=thisparams.wifislotsreq*thisparams.numofWifiUE #x1
        # x2=LTErequested=thisparams.LTEslotsreq*thisparams.numofLTEUE #x2

        # # print("\nx1",x1,"\nx2",x2,"\ny1",y1,"\ny2",y2,"\n")

        # # # Fairness index calculation

        # f1=LTECountS/(thisparams.LTEslotsreq*thisparams.numofLTEUE)
        # f2=WifiCountS/(thisparams.wifislotsreq*thisparams.numofWifiUE)
        # fair = (f1+f2)**2/(2*((f1)**2+(f2)**2))
        # Fairness.append(fair)
        # print("Fairness: ",fair)

        print("-------------------------------------------------------")
            