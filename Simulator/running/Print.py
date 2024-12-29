# This class holds the flags to enable/disable printing values in main function of simulator
class Verbose:
    LTE_BS_info = 1
    Wifi_BS_info = 1

    profile_and_probability = 1
    LTE_user_data_rates = 1
    Wifi_user_data_rates = 1
    
    LTE_user_SINR_MCS_value = 1 
    Wifi_user_SNR_MCS_value = 1 
    
    LTE_user_req_PRB = 1 # use with printing 
    Wifi_user_req_slots = 1 # use with printing SNR MCS

    LTE_BS_Req_by_user = 1
    Wifi_BS_Req_by_user = 1

    CSMA_CA_Logs = 0
    LTE_proportions = 0

    vary_factor = 0

    frame_dictionary = 0

    state_action_Qtable = 0
    Qtable = 0


    plot_Scene = 1 # plotting graph of positioning of BS and UE in the scene
    plot_SINR_Count = 0 # plot number of LTE users vs SINR
    plot_SNR_Count = 0 # plot number of Wifi users vs SNR

    # end
    Table_Fairness_LTH_WTH = 0
    List_line_Fairness = 0  # prints long list of fairness values of each iteration
    List_line_LTE_throughput = 0  # prints long list of LTE throughput values of each iteration
    List_line_Wifi_throughput = 0  # prints long list of LTE throughput values of each iteration

    FairnessVsFrameIters = 1
