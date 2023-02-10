# This class holds the flags to enable/disable printing values in main function of simulator
class Verbose:
    profile_and_probability = 1
    LTE_user_data_rates = 1
    Wifi_user_data_rates = 1
    LTE_user_SINR_MCS_value = 1 
    Wifi_user_SNR_MCS_value = 1 
    LTE_user_req_PRB = 1 # use with printing 
    Wifi_user_req_slots = 1 # use with printing SNR MCS

    plot_Scene = 0  # plotting graph of positioning of BS and UE in the scene
    plot_SINR_Count = 0 # plot number of LTE users vs SINR
    plot_SNR_Count = 0 # plot number of Wifi users vs SNR
