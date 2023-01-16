import math

class PARAMS:
    numofLTEBS = 3
    numofWifiBS = 3
    numofLTEUE = 1
    numofWifiUE = 1
    const=90
    subframe=1000 #1ms = 1000us 
    wifiuserslot=9 #9us==1slot(used by us) in wifi 
    wifislotsreq=90 #Wifi slots(9us) required per user
    LTEslotsreq=0.5 #LTE slots(0.5ms) required per user
    length = 100
    breadth = 100
    prob = 0.5
    pTxWifi = .19    # Unit: Watt
    pTxLTE = .19   # Unit: Watt
    # temp_noise = -90    # Unit: dBm/Hz
    noise=-96


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