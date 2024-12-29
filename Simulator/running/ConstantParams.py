import math

class PARAMS:

    scene = 1
    numofLTEBS = 1
    numofWifiBS = 1
    numofLTEUE = 30
    numofWifiUE = 15
    
    times_frames = 15000    # Simulate for this value x 10ms

    vary_load = 0   # set this flag to vary the load in iterations
    vary_for_every = 100    # Load will be changed for these many frame iterations

    set_users_LTE  = [10,9,11,12,9,1,100,5,6]
    set_users_Wifi = [6,5,100,1,9,12,11,9,10]

    vary_iterator = 0   # iterates in the set user list
    # decrease_factors = [0.5, 0.6, 0.7, 0.8, 0.9,1]
    # increase_factors = [1.1, 1.2, 1.3, 1.4, 1.5]

    length = 100
    breadth = 100
    
    prob = 0.5

    pTxWifi = .19    # Unit: Watt
    pTxLTE = .19   # Unit: Watt
    noise = -80

    duration_frame = 10 # 10 ms
    duration_subframe = 1   # 1 ms
    duration_slot = 0.5 # 0.5 ms

    duration_wifislot = 9   # 9 us

    wifi_slots_per_subframe = math.floor((duration_subframe*1000)/duration_wifislot)

    PRB_symbols = 7 # this is 7 symbols per resource block
    PRB_subcarriers = 12 # this is 12 subcarriers per resource block (derived value)
    
    PRB_total_symbols = PRB_subcarriers*PRB_symbols

    PRB_subcarrier_bandwidth = 15 # KHz
    PRB_bandwidth = 180 # KHz

    PRB_total_prbs = 100

    pTx_one_PRB = pTxLTE/(2*PRB_total_prbs*duration_frame*100)

    LTEprofiles = [128,256,512,1024]
    Wifiprofiles = [256,512,1024,2048]
    LTE_ratios = [4,3,2,1]
    wifi_ratios = [1,2,3,4]
    LTE_profile_prob = []
    wifi_profile_prob = []
    LTE_profile_c_prob = []
    wifi_profile_c_prob = []
    seed_valueLTE = 10
    seed_valueWifi = 10

    LTE_MCS = {-6.936:0.1523,-5.147:0.2344,-3.18:0.377,-1.253:0.6016,0.761:0.877,2.699:1.1758,4.694:1.4766,6.525:1.9141,8.573:2.4063,10.366:2.7305,12.289:3.3223,14.173:3.9023,15.888:4.5234,17.814:5.1152,19.829:5.5547, 21:6.5,22:7.5}
    wifi_MCS = {2:7.2, 5:14.4, 9:21.7, 11:28.9, 15:43.3, 18:57.8, 20:65.0, 25:72.2, 29:86.7}

    backoff_lower = 5
    backoff_upper = 20

    SIFS = 1    # Slots
    DIFS_slots = 2 + SIFS    # Slots

    def get_bits_per_slot_from_Kbps(self,value_Kbps):

        return (value_Kbps/2)
    
    def get_bits_per_wifi_slot_from_Mbps(self,value_Mbps):

        # Ex: 128 Mbps to bits per wifi slot (bits/9 us)
        # 128 * 10^6 bits 10^-6 us
        # 128  * 9 (bits/nine-us)

        return (value_Mbps*9)

    def get_dB_from_dBm(self,value_dBm):
        return (value_dBm-30)

    def get_dBm_from_Watt(self,value_watt):
        return (10*math.log(value_watt*1000,10))

    def get_dB_from_Watt(self,value_watt):
        val_dB = 10*math.log(value_watt,10)
        return val_dB
        
    def get_Watt_from_dB(self,value_dB):
        val_Watt = 10**(value_dB/10)
        return val_Watt

    def get_mWatt_from_dBm(self,value_dBm):
        val_mWatt = 10**(value_dBm/10)
        return val_mWatt/1000

    # noise = get_dBm_from_Watt((get_Watt_from_dBm(PARAMS().temp_noise)*20*(10**6)))#convert to dbm from watt (get watt from dbm(temp_noise) *20*10^6)