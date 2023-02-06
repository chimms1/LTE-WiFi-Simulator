import math

class PARAMS:

    scene = 0
    numofLTEBS = 1
    numofWifiBS = 1
    numofLTEUE = 10
    numofWifiUE = 10
    const=90
    subframe=1000 # 1ms = 1000us 
    wifiuserslot=9 # 9us==1slot(used by us) in wifi 
    wifislotsreq=90 # Wifi slots(9us) required per user
    LTEslotsreq=0.5 # (Will be deprecated soon) LTE slots(0.5ms) required per user
    length = 100
    breadth = 100
    prob = 0.5
    pTxWifi = .19    # Unit: Watt
    pTxLTE = .19   # Unit: Watt
    noise=-96

    PRB_symbols = 7 # this is 7 symbols per resource block
    PRB_subcarriers = 12 # this is 12 subcarriers per resource block (derived value)
    
    PRB_total_symbols = PRB_subcarriers*PRB_symbols

    PRB_subcarrier_bandwidth = 15 # KHz
    PRB_bandwidth = 180 # KHz

    profiles = [64,128,256,1000]
    LTE_ratios = [4,3,2,1]
    wifi_ratios = [2,3,4,1]
    LTE_profile_prob = []
    wifi_profile_prob = []
    LTE_profile_c_prob = []
    wifi_profile_c_prob = []

    LTE_MCS = {-6.936:0.1523,-5.147:0.2344,-3.18:0.377,-1.253:0.6016,0.761:0.877,2.699:1.1758,4.694:1.4766,6.525:1.9141,8.573:2.4063,10.366:2.7305,12.289:3.3223,14.173:3.9023,15.888:4.5234,17.814:5.1152,19.829:5.5547}
    # wifi_MCS = {}


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