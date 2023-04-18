import numpy as np
import pandas as pd
import math
from tqdm import tqdm
from collections import Counter
import copy

from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass
from running.ServiceClass import GraphService
from running.Print import Verbose
from entities.UserEquipment import WifiUserEquipment

from Qlearning.learning import learning


def count_users(bs_array):
    usercount = 0
    for b in bs_array:
        usercount += len(b.t_user_list)
    
    return usercount

# Get original user (returns object) from copy of user
def bringRealUser(selected_user,wuss):

    for u in wuss:
        if u.ueID == selected_user.ueID:
            return u

if __name__ == "__main__":
    print("Hello World!")

    # for num in userscenes:
    thisparams = PARAMS()   # this is object of constant params to be used in main

    service = ServiceClass()
    graphservice = GraphService()
    verbose = Verbose()

    rl = learning()

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
    
    if thisparams.vary_load == 1:
        if len(thisparams.set_users_Wifi) == ((thisparams.times_frames/thisparams.vary_for_every)-1) and len(thisparams.set_users_LTE) == ((thisparams.times_frames/thisparams.vary_for_every)-1):
            print("Number of users will be varied for every {}th iteration".format(thisparams.vary_for_every))
        else:
            print("Error: Vary for every iteration and number of user counts are mismatched")
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
    
    if verbose.LTE_BS_info == 1:
        print("\n=== LTE BS ===")
        for b in lbss:
            print("LTE BSid {}: User ids Connected: {}".format(b.bsID,[u.ueID for u in b.t_user_list]))
        print("======")

    if verbose.Wifi_BS_info == 1:
        print("\n=== Wifi BS ===")
        for b in wbss:
            print("Wifi BSid {}: User ids Connected: {}".format(b.bsID,[u.ueID for u in b.t_user_list]))
        print("======")

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

    # for u in luss:

    #     print("LTE userid {}: {:.4f}".format(u.ueID,u.SINR))


    if verbose.LTE_BS_Req_by_user == 1:
        print("\n=== LTE BS Dictionary of User req bits ===")
        for b in lbss:
            
            users = b.bits_per_symbol_of_user.keys()
            print("LTE BSid {}".format(b.bsID))
            for u in users:

                print(" @> {}:{}".format(u.ueID,b.bits_per_symbol_of_user[u]))

        print("======")


    service.calculate_LTE_user_PRB(thisparams, luss)



    if verbose.LTE_user_SINR_MCS_value == 1:
        print("\n=== LTE user SINR and MCS value ===")
        for b in lbss:
            for u in b.user_list:
                print("LTE userid {}: {:.4f} @> {} bits per symbol".format(u.ueID,u.SINR,b.bits_per_symbol_of_user[u]))
                if verbose.LTE_user_req_PRB == 1:
                    print("Required PRBs: {}".format(u.req_no_PRB))
        
        print("\nTotal Required PRBs: {}".format(service.getTotalRequiredPRB(thisparams, luss)))
        print("======")
    
    x1_numerator = service.getTotalRequiredPRB(thisparams, luss)

    #
    # Measuring SNR for Wifi Users
    for u in wuss:
        u.measureSNR()
        SNR.append(u.SNR)

    service.decide_wifi_bits_per_symbol(wbss, thisparams)
    
    for u in wuss:
        print("Wifi userid {}: {:.4f}".format(u.ueID,u.SNR))

    if verbose.Wifi_BS_Req_by_user == 1:
        print("\n=== Wifi BS Dictionary of User req bits ===")
        for b in wbss:
            
            users = b.bits_per_symbol_of_user.keys()
            print("Wifi BSid {}".format(b.bsID))
            for u in users:

                print(" @> {}:{}".format(u.ueID,b.bits_per_symbol_of_user[u]))

        print("======")

    service.calculate_wifi_user_slots(thisparams, wuss)

    if verbose.Wifi_user_SNR_MCS_value == 1:
        print("\n=== Wifi user SNR and MCS value ===")
        for b in wbss:
            for u in b.user_list:
                print("Wifi userid {}: {:.4f} @> {} Mbps".format(u.ueID,u.SNR,b.bits_per_symbol_of_user[u]))
                if verbose.Wifi_user_req_slots == 1:
                    print("Required wifi slots: {}".format(u.req_no_wifi_slot))
        print("\nTotal Required wifi slots: {}".format(service.getTotalRequiredWifiSlot(thisparams, wuss)))
        print("======")
    
    x2_numerator = service.getTotalRequiredWifiSlot(thisparams, wuss)

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
    format=[[0,1,1,1,1,0,1,1,1,1], # 8:2  9:8       444:01      8:90 
            [0,1,1,1,0,0,1,1,1,0], # 6:4  7:16      333:01      16:90
            [0,1,1,0,0,0,1,1,0,0], # 4:6  4:24      222:01      24:90
            [0,1,1,1,1,0,0,0,0,0], # 4:6  4:24      222:01      24:90
            [0,1,1,1,0,0,0,0,0,0], # 3:7  3:28      166.5:01    28:90        
            [0,1,1,0,0,0,0,0,0,0], # 2:8  2:32      111:01      32:90
            [0,1,1,1,1,0,1,1,1,0]] # 7:3  8:12      388.5:01    12:90

    format_fairness = {}
    format_U_LTE = {}
    format_power = {}
    #============================================================
    # Modifiying for multiple base stations

    # formats_required = int(input("Enter the number of formats to simulate[1-7]: "))

    # print("\nFormats available:\n")
    # for count in range(0,len(format)):
    #     print("[{}]: {}".format(count,format[count]))

    # while 1:
    #     print("\n-- Choose {} formats from above --".format(formats_required))
    #     user_formats = list(input("Enter space separated choices => ").split())

    #     user_formats = [int(x) for x in user_formats]

    #     print("Formats chosen ",user_formats)

    #     if len(user_formats) != formats_required:
    #         print("Expected {} formats... but {} were given".format(formats_required,len(user_formats)))
    #         continue

    #     invalid_format = 0
    #     for num in user_formats:
    #         if num>6 or num<0:
    #             print("Invalid format choice...try again")
    #             invalid_format = 1
    #             break

    #     if invalid_format:
    #         continue
    #     else:
    #         break

    # print("========================================")

    # combos = list(service.my_combinations_with_replacement(user_formats,thisparams.numofLTEBS))

    # print("Generated index Combinations: ")
    # for combo in combos:
    #     print(combo)


    # print("\nStoring frame structure combinations:")
    # chosen_formats = []
    # for combo in combos:
    #     temp_list = []
    #     for index in combo:
    #         temp_list.append(format[index])
    #     chosen_formats.append(temp_list)
    
    # for x in chosen_formats:
    #     print(x)

    print("=============================================================================")
    

    # print("LTE users: {} Wifi users: {}".format(count_users(lbss),count_users(wbss)))

    # print("Copy LTE users: {} Wifi users: {}".format(count_users(copy_lbss),count_users(copy_wbss)))
    # exit()

    Fairness = []   # Stores fairness for each frame combination
    LTE_Throughput = [] # Stores throughput of LTE
    LTE_Power = []

    Wifi_Throughput = [] # Stores total throughput of Wifi


    #Simulation starts
    # for simulation_iterator in range(0,len(chosen_formats)):

    # for b in lbss:
    #     b.lusscount=b.lusscount2


    for b in wbss:
        b.t_user_list = b.user_list
    
    allwuss = []

    for u in wuss:
        # tempu = WifiUserEquipment()
        tempu = copy.copy(u)

        allwuss.append(tempu)
    

    # print("\n\n-----------------Combination {}---------------------".format(simulation_iterator))

    # print(" iter: {} LTE users: {} Wifi users: {}".format(simulation_iterator,count_users(lbss),count_users(wbss)))
    print("LTE users: {} Wifi users: {}".format(count_users(lbss),count_users(wbss)))

    # Select combination
    # assigner = 0
    # for b in lbss:
    #     b.format = chosen_formats[simulation_iterator][assigner]
    #     assigner+=1
    
    # Do work
    # LTECountS=0
    # LTECountU=0

    # WifiCountS=0
    # WifiCountU=0

    channel_busy = 0

    CTS = 0
    tuserlist = []
    RTSuserlist = []
    FinishedWifilist = []
    # FinishedLTElist = []

    # total_PRBs = 0
    # total_Wifi_slots = 0

    vary_for_every = 1

    # if thisparams.vary_load == 1:
    
    vary_for_every = thisparams.vary_for_every
    
    Wifi_vary_factor = 1 #   initially set to 1
    LTE_vary_factor = 1

    lbss[0].format = format[rl.initial_state]

    for tf in tqdm(range(0,thisparams.times_frames)):

        if tf>rl.exploration:
            rl.Epsilon = 0.95
        
        if tf>thisparams.vary_from:
            thisparams.vary_load = 1
        
        p = rl.ChoosePtoDecideAction()

        rl.ChooseAction(p)
        rl.PerformAction()

        if verbose.each_action == 1:
            print("\nChoosen Action: ",rl.current_action)
            print("New State: ",rl.current_state)
            print("Frame: ",rl.current_frame)

        lbss[0].format = format[rl.current_frame]

        if rl.current_action == 2 or rl.current_action == -2:
            thisparams.pTxLTE = rl.original_power/rl.current_pFactor
            
            lbss[0].pTx = thisparams.pTxLTE

            thisparams.pTx_one_PRB = thisparams.pTxLTE/(2*thisparams.PRB_total_prbs*thisparams.duration_frame*100)

            for lb in lbss:
                lb.bits_per_symbol_of_user = dict()
            
            # Measuring SINR for LTE Users
            for u in luss:
                u.measureSINR(wbss)

            service.decide_LTE_bits_per_symbol(lbss,thisparams)
            service.calculate_LTE_user_PRB(thisparams, luss)
            
            if verbose.each_action == 1:
                print("New Power: ",thisparams.pTxLTE)
                print("Total Required PRBs: {}".format(service.getTotalRequiredPRB(thisparams, luss)))
        
        
        
        LTECountS=0
        LTECountU=0

        WifiCountS=0
        WifiCountU=0

        LTEPowerS = 0.0

        total_PRBs = 0  # Holds total PRBs allocated for LTE in 10ms
        total_Wifi_slots = 0    # Holds total slots allocated for Wifi in 10ms

        total_LTE_bits_sent = 0 # Holds bits sent by LTE users
        total_Wifi_bits_sent = 0 # Holds bits sent by Wifi users
        
        if verbose.CSMA_CA_Logs == 1:
            print("------------------------------------------------------------------------------------------- {}".format(tf))
        
        
        for subframe_iterator in range(0,10):
            
            # Add users back to initial state
            if subframe_iterator == 0:

                # if thisparams.vary_load == 0:
                CTS = 0

                for u in FinishedWifilist:
                    allwuss.append(u)

                for u in tuserlist:
                    allwuss.append(u)

                for u in RTSuserlist:
                    allwuss.append(u)
                
                is_selected_user_present = 0

                if tf >0:
                    for u in allwuss:
                        if selected_user.ueID == u.ueID:
                            is_selected_user_present = 1
                            break
                    
                    if is_selected_user_present == 1:
                        pass
                    else:
                        selected_user.req_no_wifi_slot = (selected_user.req_data_rate*10)/(selected_user.bs.bits_per_symbol_of_user[bringRealUser(selected_user, wuss)]*9)
                        selected_user.req_no_wifi_slot = int(math.ceil(selected_user.req_no_wifi_slot))
                        allwuss.append(selected_user)

                for u in allwuss:
                    u.DIFS_flag = 0
                    u.DIFS_slots = thisparams.DIFS_slots
                    u.random_backoff_flag = 0
                    u.random_backoff_slots = 0

                FinishedWifilist = []
                tuserlist = []
                RTSuserlist = []

                for b in lbss:
                    for u in b.t_user_list:
                        u.transmission_finished = 0
                        service.calculate_LTE_user_PRB(thisparams,[u])

                ###### HERE, Varying of Users starts
                if thisparams.vary_load == 1 and vary_for_every <=0 and thisparams.vary_iterator<=0:
                        
                        

                        # LTE_vary_factor = service.Vary_Load(thisparams, LTE_vary_factor)
                        # Wifi_vary_factor = service.Vary_Load(thisparams, Wifi_vary_factor)

                        # Caluclate new count of users
                        # newLTEuserscount = math.ceil(LTE_vary_factor*thisparams.numofLTEUE)
                        # newWifiuserscount = math.ceil(Wifi_vary_factor*thisparams.numofWifiUE)
                        CTS = 0

                        newLTEuserscount = thisparams.set_users_LTE[thisparams.vary_iterator]
                        newWifiuserscount = thisparams.set_users_Wifi[thisparams.vary_iterator]

                        thisparams.vary_iterator += 1

                        # Clear older lists
                        for lb in lbss:
                            lb.user_list = np.array([])
                            lb.t_user_list = np.array([])
                            lb.bits_per_symbol_of_user = dict()
                        
                        for wb in wbss:
                            wb.user_list = np.array([])  
                            wb.t_user_list = np.array([])
                            wb.bits_per_symbol_of_user = dict()

                        allwuss = []
                        tuserlist = []
                        RTSuserlist = []
                        FinishedWifilist = []

                        # Create new users
                        varyparams = PARAMS()
                        varyparams.numofLTEUE = newLTEuserscount
                        varyparams.numofWifiUE = newWifiuserscount

                        luss = service.createLTEUsers(varyparams)
                        wuss = service.createWifiUsers(varyparams)

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

                        # Based on ratios decided by the user, assign data rates to UE
                        service.assign_data_rate_to_users(thisparams, luss, wuss)

                        SINR=[]
                        SNR=[]

                        # Measuring SINR for LTE Users
                        for u in luss:
                            u.measureSINR(wbss)
                            SINR.append(u.SINR)

                        service.decide_LTE_bits_per_symbol(lbss,thisparams)
                        service.calculate_LTE_user_PRB(thisparams, luss)

                        for u in wuss:
                            u.measureSNR()
                            SNR.append(u.SNR)

                        service.decide_wifi_bits_per_symbol(wbss, thisparams)
                        service.calculate_wifi_user_slots(thisparams, wuss)

                        for b in wbss:
                            b.t_user_list = b.user_list
                        
                        allwuss = []

                        for u in wuss:
                            # tempu = WifiUserEquipment()
                            tempu = copy.copy(u)

                            allwuss.append(tempu)

                            
                        mykeys = list(format_fairness.keys())
                        mykeys.sort()


                        print({w: format_fairness[w] for w in mykeys})
                        print("")
                        print({w: format_U_LTE[w] for w in mykeys})
                        print("")
                        print({w: format_power[w] for w in mykeys})
                        print("")

                        format_fairness  = {}
                        format_U_LTE = {}
                        format_power = {}

                        arrow = {0:"⬅️",1:"🔄",2:"➡️",3:"⬇️",4:"⬆️"}

                        arrowstates = {}
                        temp_state = rl.current_state

                        for st in range(0,21):

                            rl.current_state = st
                            max_action = rl.getMaxActionInd()

                            arrowstates[st] = arrow[max_action]
                        
                        for powo in range(0,3):
                            for st in range(0,7):
                                st2 = st+powo*7
                                print(st2,end="  ")
                            print("")
                            for st in range(0,7):
                                st2 = st+powo*7
                                print(arrowstates[st2],end="  ")
                            print("\n")
                        rl.current_state = temp_state
                            
                        if verbose.vary_factor == 1:
                            print("LTE users {} at iteration {}".format(varyparams.numofLTEUE,tf))
                            print("PRBs Required: {}".format(service.getTotalRequiredPRB(thisparams, luss)))
                            print("Wifi users {} at iteration {}".format(varyparams.numofWifiUE,tf))
                            print("Wifi Slots Required: {}".format(service.getTotalRequiredWifiSlot(thisparams, wuss)))

                        x1_numerator = service.getTotalRequiredPRB(thisparams, luss)
                        x2_numerator = service.getTotalRequiredWifiSlot(thisparams, wuss)

                        vary_for_every = thisparams.vary_for_every


            single_zero = 0
            multiple_zero = 0
            all_one = 0

            zero_counter = 0
            one_counter = 0

            lbs_single_zero = None

            for b in lbss:
                if b.format[subframe_iterator] == 0:
                    zero_counter += 1

                elif b.format[subframe_iterator] == 1:
                    one_counter += 1

            if zero_counter > 1:
                multiple_zero=1

            elif zero_counter == 1:
                single_zero=1
                lbs_single_transmission_ind = 0
                for b in lbss:
                    if b.format[subframe_iterator]==0:
                        break
                    lbs_single_transmission_ind+=1

            
            elif one_counter == thisparams.numofLTEBS:
                all_one=1

            # More than one LTE BS has zero
            if multiple_zero == 1 or single_zero == 1:
                channel_busy = 1
            elif all_one == 1:
                total_Wifi_slots += 111
                channel_busy = 0

            # "Simulation for one sub-frame (0/1) in a frame" ==============================
            # service.assignProb2(allwuss)

            Wifisensecount = 0
            rem_wifi_slots = thisparams.wifi_slots_per_subframe
            
            while Wifisensecount < thisparams.wifi_slots_per_subframe:

                if verbose.CSMA_CA_Logs == 1:
                    print("current wifi slot ", Wifisensecount)
                if len(allwuss) == 0 and len(tuserlist)!=0 and channel_busy==1:
                    
                    if verbose.CSMA_CA_Logs == 1:
                        print("All the remaining {} Wifi users are waiting".format(len(tuserlist)))
                    # pass
                    # do not break
                if len(allwuss)==0 and len(tuserlist)==0 and RTSuserlist ==0:
                    if verbose.CSMA_CA_Logs == 1:
                        print("All wifi users have finished transmitting and are not programmed to do it again in this simulation")
                    break   # break here


                if CTS!=0:
                    if verbose.CSMA_CA_Logs == 1:
                        print("tuserlist ",[(u.ueID) for u in tuserlist])
                        print("current status of random backoff ", [(u.ueID,u.random_backoff_slots) for u in tuserlist if u.random_backoff_flag==1])
                        print("current status of DIFS ", [(u.ueID,u.DIFS_slots) for u in tuserlist if u.DIFS_flag==1])

                    for u in tuserlist:
                            if u.random_backoff_flag == 1 and u.random_backoff_slots > 0 and u.DIFS_flag == 0:
                                u.random_backoff_slots-=1
                            
                            # Random backoff of this user become zero and now channel is busy so set randombackoff again
                            if u.random_backoff_flag == 1 and u.random_backoff_slots == 0 and u.DIFS_flag == 0:
                                u.setRandomBackoff()

                    if channel_busy == 1:
                        if verbose.CSMA_CA_Logs == 1:
                    
                            print("current status of tuserlist ", [(u.ueID,u.DIFS_slots) for u in tuserlist])
                            print("\n")
                            print(" Wifi user ",selected_user.ueID," used 1 slot during LTE's period")

                        WifiCountU+=1

                    
                    if channel_busy == 0:
                        selected_user.req_no_wifi_slot-=1
                        WifiCountS+=1

                        selected_user.bits_sent += thisparams.get_bits_per_wifi_slot_from_Mbps(selected_user.bs.bits_per_symbol_of_user[bringRealUser(selected_user,wuss)])
                        total_Wifi_bits_sent += thisparams.get_bits_per_wifi_slot_from_Mbps(selected_user.bs.bits_per_symbol_of_user[bringRealUser(selected_user,wuss)])
                        # total_Wifi_bits_sent += (selected_user.req_data_rate*9)/1000

                        if verbose.CSMA_CA_Logs == 1:
                            print(Wifisensecount," Success ",[(u.ueID,u.DIFS_slots) for u in tuserlist])
                            print(" Wifi user ",selected_user.ueID," used 1 slot successfully")

                    CTS-=1
                    # When CTS becomes zero during LTE transmission sub frame
                    if CTS==0 and channel_busy==1:
                        
                        if verbose.CSMA_CA_Logs == 1:
                            print("User ",selected_user.ueID, "was till now sending during period 0 and is added back to allwuss")
                            print("\n")
                        
                        # selected_user.req_no_wifi_slot = (selected_user.req_data_rate*10)/(selected_user.bs.bits_per_symbol_of_user[bringRealUser(selected_user, wuss)]*9)
                        # selected_user.req_no_wifi_slot = int(math.ceil(selected_user.req_no_wifi_slot))

                        allwuss.append(selected_user)
                        # FinishedWifilist.append(selected_user)

                        if verbose.CSMA_CA_Logs == 1:
                    
                            print("current status of allwuss ",[u.ueID for u in allwuss])
                        
                        continue

                    # When CTS becomes zero during Wifi transmission sub frame
                    if CTS==0 and channel_busy==0:
                        if selected_user.req_no_wifi_slot == 0:
                            if verbose.CSMA_CA_Logs == 1:
                    
                                print("User ",selected_user.ueID, "has completed his transmission compleetly and is added back to allwuss")
                            
                            selected_user.req_no_wifi_slot = (selected_user.req_data_rate*10)/(selected_user.bs.bits_per_symbol_of_user[bringRealUser(selected_user, wuss)]*9)
                            selected_user.req_no_wifi_slot = int(math.ceil(selected_user.req_no_wifi_slot))
                            # service.calculate_wifi_user_slots(thisparams, [selected_user])

                            # allwuss.append(selected_user)
                            FinishedWifilist.append(selected_user)

                            if verbose.CSMA_CA_Logs == 1:
                                print("current status of allwuss ",[u.ueID for u in allwuss])

                        elif selected_user.req_no_wifi_slot > 0:
                            allwuss.append(selected_user)

                        continue

            # else if CTS==0
                if CTS == 0:
                    if verbose.CSMA_CA_Logs == 1:
                        print("current status of random backoff", [(u.ueID,u.random_backoff_slots) for u in tuserlist if u.random_backoff_flag==1])
                        print("current status of DIFS", [(u.ueID,u.DIFS_slots) for u in tuserlist if u.DIFS_flag==1])

                    # if len(allwuss)>0:    
                    service.assignProb2(allwuss)

                    # For all users in the list(list of users with prob<threshold)
                    Wifiuserscount,a = service.countWifiUsersWhoTransmit2(allwuss)
                    if verbose.CSMA_CA_Logs == 1:
                        print("New Users who want to transmit: ",[x.ueID for x in a])

                    # if channel is busy
                    if channel_busy == 1:
                        if verbose.CSMA_CA_Logs == 1:
                            print("current status of random backoff", [(u.ueID,u.random_backoff_slots) for u in tuserlist if u.random_backoff_flag==1])
                        WifiCountU +=1
                        for u in a:
                            if u.random_backoff_flag == 0 and u.random_backoff_slots == 0 and u.DIFS_flag == 0:
                                u.random_backoff_flag = 1
                                u.setRandomBackoff()
                        
                        for u in tuserlist:
                            if u.random_backoff_flag == 1 and u.random_backoff_slots > 0 and u.DIFS_flag == 0:
                                u.random_backoff_slots-=1
                            if u.random_backoff_flag == 1 and u.random_backoff_slots == 0 and u.DIFS_flag == 0:
                                u.random_backoff_flag = 1
                                u.setRandomBackoff()
                            
                            if u.random_backoff_flag == 0 and u.random_backoff_slots == 0 and u.DIFS_flag == 0:
                                u.random_backoff_flag = 1
                                u.setRandomBackoff()
            
                    for u in a:
                        tuserlist.append(u)
                        allwuss.remove(u)
                        

                    # if channel is free
                    if channel_busy == 0:
                        if verbose.CSMA_CA_Logs == 1:
                            print("current status of random backoff", [(u.ueID,u.random_backoff_slots) for u in tuserlist if u.random_backoff_flag==1])

                        remove_from_tuserlist_RTS = []
                        for u in tuserlist:
                            if u.random_backoff_flag == 1 and u.random_backoff_slots > 0 and u.DIFS_flag == 0:
                                u.random_backoff_slots-=1

                            # if random
                            elif u.random_backoff_flag == 1 and u.random_backoff_slots == 0 and u.DIFS_flag == 0:
                                u.random_backoff_flag = 0
                                u.DIFS_flag = 1
                                u.DIFS_slots = thisparams.DIFS_slots

                            if u.random_backoff_flag == 0 and u.DIFS_flag == 1:
                                if u.DIFS_slots > 0:
                                    u.DIFS_slots -=1
                                
                                if u.DIFS_slots == 0:
                                    u.DIFS_flag = 0
                                    u.DIFS_slots = thisparams.DIFS_slots
                                    # send RTS
                                    RTSuserlist.append(u)
                                    remove_from_tuserlist_RTS.append(u)

                        for u in remove_from_tuserlist_RTS:
                            tuserlist.remove(u)
                        
                        if len(RTSuserlist)>0:
                            selected_user = service.sendRTS(thisparams,RTSuserlist)
                            selected_user.RTS_flag=1

                            RTSuserlist.remove(selected_user)
                            # tuserlist.remove(selected_user)

                            if verbose.CSMA_CA_Logs == 1:
                                print("Selected userid: {} ".format(selected_user.ueID))
                            
                            CTS = selected_user.req_no_wifi_slot
                            t_req_no_wifi_slot=selected_user.req_no_wifi_slot
                        else:
                            WifiCountU+=1

                    # <check for empty slot here>
                Wifisensecount+=1
                rem_wifi_slots-=1

                
            # End of while 111
            if verbose.CSMA_CA_Logs == 1:
                print("\nWifi Successful: ",WifiCountS," Wifi Unused: ",WifiCountU,"\n")
    
            # More than one LTE BS has zero
            if multiple_zero == 1:
                LTECountU+=4
                continue
            
            
            elif single_zero == 1:
                LTEsubframeS = 0
                half_ms = 2
                while half_ms:
                    LTE_proportions = []
                    selected_bs = lbss[lbs_single_transmission_ind]

                    LTE_proportions = service.calculate_LTE_proportions(thisparams,selected_bs.t_user_list)
                    
                    if verbose.LTE_proportions==1:
                        print(LTE_proportions)


                    give = 0
                    for u in selected_bs.t_user_list:
                        if u.transmission_finished == 1:
                            continue

                        if verbose.LTE_proportions==1:
                            print(u.req_no_PRB,LTE_proportions[give])

                        if u.req_no_PRB <= LTE_proportions[give] :
                            givenPRB = u.req_no_PRB
                            u.req_no_PRB = 0
                            u.transmission_finished = 1
                            
                            u.bits_sent += givenPRB*thisparams.PRB_total_symbols*u.bs.bits_per_symbol_of_user[u]
                            total_LTE_bits_sent += givenPRB*thisparams.PRB_total_symbols*u.bs.bits_per_symbol_of_user[u]

                            LTECountS += givenPRB
                            LTEsubframeS+=givenPRB

                            service.calculate_LTE_user_PRB(thisparams,[u])  # user goes back and comes back again with same requirement
                            # u.req_no_PRB = (u.req_data_rate*(10**3)*10*(10**-3))/(u.bs.bits_per_symbol_of_user[u]*thisparams.PRB_total_symbols)
                            # u.req_no_PRB = int(LTE_vary_factor*math.ceil(u.req_no_PRB))

                            if u.req_no_PRB <=0:
                                u.req_no_PRB = 1

                        else:
                            u.req_no_PRB -= LTE_proportions[give]
                            u.bits_sent += LTE_proportions[give] * thisparams.PRB_total_symbols * u.bs.bits_per_symbol_of_user[u]
                            total_LTE_bits_sent += LTE_proportions[give]*thisparams.PRB_total_symbols*u.bs.bits_per_symbol_of_user[u]

                            LTECountS += LTE_proportions[give]
                            LTEsubframeS += LTE_proportions[give]

                        give+=1

                    total_PRBs += 100
                    half_ms -= 1
                
                    if verbose.LTE_proportions==1:
                        print("Successful RB allocation till now: ",LTECountS)
                
                LTEPowerS += LTEsubframeS*thisparams.pTx_one_PRB
                if verbose.LTE_proportions == 1:
                    print("Power consumed this subframe: ",LTEsubframeS*thisparams.pTx_one_PRB)

            
        #
        # End of subframe iteration loop

        # "This fairness calculation is only for one frame"
        # for the current frame
        U_LTE = LTECountS/total_PRBs

        zeroes = {0:2,1:4,2:6,3:6,4:7,5:8,6:3}
        # x1 = x1_numerator/0.0019
        x1 = x1_numerator/total_PRBs

        U_Wifi = WifiCountS/total_Wifi_slots
        
        x2 = x2_numerator/total_Wifi_slots

        frame_fairness = ((x1+x2)**2)/(2*((x1**2)+(x2**2)))

        Fairness.append(frame_fairness)

        format_fairness[rl.current_state] = frame_fairness
        format_U_LTE[rl.current_state] = U_LTE
        format_power[rl.current_state] = LTEPowerS

        rl.UpdateQtable(frame_fairness, LTEPowerS, thisparams)

        # "This throughput calculation is only for one frame"
        # for the current frame
        frame_T_LTE = (total_LTE_bits_sent * 10**3)/thisparams.duration_frame
        LTE_Throughput.append(frame_T_LTE)
        LTE_Power.append(LTEPowerS)

        frame_T_Wifi = (total_Wifi_bits_sent * 10**3)/thisparams.duration_frame
        Wifi_Throughput.append(frame_T_Wifi)

        if verbose.LTE_Power_Frame == 1:
            print("LTE Power Consumed this Frame ",LTEPowerS)
        
        if verbose.CSMA_CA_Logs == 1:
            print("current status of allwuss ",[u.ueID for u in allwuss])
            print("current status of DIFS ", [(u.ueID,u.DIFS_slots) for u in tuserlist if u.DIFS_flag==1])
            # print("current status of random backoff ", [(u.ueID,u.random_backoff_slots) for u in tuserlist])
            print("current status of random backoff ", [(u.ueID,u.random_backoff_slots) for u in tuserlist if u.random_backoff_flag==1])
            print("current status of RTSuserlist ",[u.ueID for u in RTSuserlist])

        if verbose.state_action_Qtable == 1:
            print("Previous State: {} -> Current State: {} Action: {}\n".format(rl.previous_state,rl.current_state,rl.current_action))
            for state in range(0,7):
                for action in range(0,3):
                    print("{:.4f}".format(rl.Q_Table[state][action]),end=" ")
                print("\n")
            print("\n")

        if thisparams.vary_load == 1:
            vary_for_every-=1
        #
        # End of times_frame loop

        
        # print("\n\n-----------------Combination {}---------------------".format(simulation_iterator))
        # print("LTE slots used ",LTECountS) #" LTE slots unused ",LTECountU)
        # print("Wifi slots used ",WifiCountS," Wifi slots unused ",WifiCountU)

        # print("Total Wifi slots ",total_Wifi_slots," Total PRBs ",total_PRBs)


        # # "This fairness calculation is only for one frame"
        # # for the current frame
        # U_LTE = LTECountS/total_PRBs
        # U_Wifi = WifiCountS/total_Wifi_slots

        # frame_fairness = ((U_LTE+U_Wifi)**2)/(2*((U_LTE**2)+(U_Wifi**2)))
        
        # print(frame_fairness)

        # Fairness.append(frame_fairness)
        # print("-------------------------------------------------------")
    
    if verbose.frame_dictionary == 1:
        
        mykeys = list(format_fairness.keys())
        mykeys.sort()


        print({w: format_fairness[w] for w in mykeys})
        print("")
        print({w: format_U_LTE[w] for w in mykeys})
        print("")
        print({w: format_power[w] for w in mykeys})



    if verbose.Qtable==1:
        print("-------------------------------------------------------")
        print("Final State: {}\n".format(rl.current_state))
        print("\tBack     Stay   Front   Down     Up")
        for state in range(0,21):
            print(state," ==> ",end = " ")
            for action in range(0,5):
                print("{:.4f}".format(rl.Q_Table[state][action]),end=" ")
            print("\n")

        arrow = {0:"⬅️",1:"🔄",2:"➡️",3:"⬇️",4:"⬆️"}

        arrowstates = {}

        for st in range(0,21):

            rl.current_state = st
            max_action = rl.getMaxActionInd()

            arrowstates[st] = arrow[max_action]
        
        for powo in range(0,3):
            for st in range(0,7):
                st2 = st+powo*7
                print(st2,end="  ")
            print("")
            for st in range(0,7):
                st2 = st+powo*7
                print(arrowstates[st2],end="  ")
            print("\n")

    print("-------------------------------------------------------")

    
    if verbose.Table_Fairness_LTH_WTH==1:
        print("Fairness  LT  WT")

        for i in range(0,thisparams.times_frames):
            print("{:.4f}      {:.4f}  {:.4f}".format(Fairness[i],LTE_Throughput[i],Wifi_Throughput[i]))

    
        print("-------------------------------------------------------",end="\n\n")

    if verbose.List_line_Fairness==1:
        print("-------------------------------------------------------")
        for f in Fairness:
            print(f)
        print("-------------------------------------------------------")

    if verbose.List_line_LTE_throughput==1:
        print("-------------------------------------------------------")
        for f in LTE_Throughput:
            print(f)
        print("-------------------------------------------------------")
    
    if verbose.List_line_LTE_Power==1:
        print("-------------------------------------------------------")
        for f in LTE_Power:
            print(f)
        print("-------------------------------------------------------")

    if verbose.List_line_Wifi_throughput==1:
        print("-------------------------------------------------------")
        for f in Wifi_Throughput:
            print(f)
        print("-------------------------------------------------------")
    
    if verbose.FairnessVsFrameIters == 1:
        graphservice.PlotFairnessFrameIters(Fairness,thisparams.times_frames,thisparams)