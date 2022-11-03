import numpy as np
from running.ConstantParams import PARAMS
from running.ServiceClass import ServiceClass
from running.ServiceClass import GraphService

if __name__ == "__main__":
    print("Hello World!")

    service = ServiceClass()
    graphservice = GraphService()
    SINR=[]
    SNR=[]

    scene = 3
    description = "multiple"

    # Create BS and UE using Service Class
    lbss = service.createLTEBaseStations(scene)
    wbss = service.createWifiBaseStations(scene)

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
        print("\nINDEX:", ind)

        # Add this UE to user_list
        wbss[ind].user_list = np.append(wbss[ind].user_list, u)


    # Measuring SINR for LTE Users
    for u in luss:
        u.measureSINR(wbss)
        SINR.append(u.SINR)

    # Measuring SNR for Wifi Users
    for u in wuss:
        u.measureSNR()
        SNR.append(u.SNR)

    # Creating CSVs
    service.createLocationCSV(wbss, lbss, luss, wuss)

    # Plotting Graphs for scenes
    graphservice.PlotScene(scene, description)


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

    print("tttttttttttttttttttttttttttttttttttttttttt\n\n")
    graphservice.PlotHistSINR(SINR)
    # graphservice.PlotHistSINR(SINR)
    print("\n\nbeech me\n\n")
    graphservice.PlotHistSNR(SNR)
    # graphservice.PlotHistSNR(SNR)