import math

class PARAMS:
    numofLTEBS = 1
    numofWifiBS = 1
    numofLTEUE = 50
    numofWifiUE = 50
    length = 100
    breadth = 100
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

