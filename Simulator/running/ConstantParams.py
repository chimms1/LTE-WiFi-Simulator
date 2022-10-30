import math

class PARAMS:
    numofLTEBS = 1
    numofWifiBS = 1
    numofLTEUE = 50
    numofWifiUE = 50
    length = 100
    breadth = 100
    pTxWifi = 20    # Unit: Watt
    pTxLTE = 20     # Unit: Watt
    noise = -120     # Unit: dBm


    def get_dB_from_dBm(self,value_dBm):
        return (value_dBm-30)

    def get_dBm_from_Watt(self,value_watt):
        return (10*math.log(value_watt,10))

    def get_dB_from_Watt(self,value_watt):
        val_dBm = 10*math.log(value_watt,10)
        val_dB = val_dBm - 30
        return val_dB