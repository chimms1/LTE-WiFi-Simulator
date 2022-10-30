import numpy as np
import pandas as pd
from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass

if __name__ == "__main__":
    print("Hello World!")

    service = ServiceClass()

    # Create BS and UE using Service Class
    lbss = service.createLTEBaseStations()
    wbss = service.createWifiBaseStations()

    luss = service.createLTEUsers()
    wuss = service.createWifiUsers()

    # Connecting all the LTE UE with a LTE BS
    for u in luss:
        ind = u.measurePowerRcvd(lbss)

        # Add this UE to user_list
        lbss[ind].user_list = np.append(lbss[ind].user_list, u)

    # Connecting all the Wifi UE with a Wifi BS
    for u in wuss:
        ind = u.measurePowerRcvd(wbss)

        # Add this UE to user_list
        wbss[ind].user_list = np.append(wbss[ind].user_list, u)


    # Measuring SINR for LTE Users
    for u in luss:
        u.measureSINR(wbss)

    # Measuring SNR for Wifi Users
    for u in wuss:
        u.measureSNR()

    # Creating CSVs
    service.createLocationCSV(wbss, lbss, luss, wuss)



    # Printing

    print("x\ty of LTE Base Stations")
    for b in lbss:
        print("{}\t{}\t SINR = {}".format(b.x, b.y, b.SINR))

    print("x\ty of Wifi Base Stations")
    for b in wbss:
        print("{}\t{}\t SNR = {}".format(b.x, b.y, b.SNR))

    print("\n\n")

    print("\n\n\nx\ty of LTE User Equipments\n")
    for u in luss:
        print("{}\t{}\tLTE-bs: {} SINR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SINR))

    print("\n\n\nx\ty of Wifi User Equipments\n")
    for u in wuss:
        print("{}\t{}\t Wifi-bs: {} SNR: {:.4f}".format(u.x, u.y, u.bs.bsID, u.SNR))
