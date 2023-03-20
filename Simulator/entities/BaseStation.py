import numpy as np
from running.ConstantParams import PARAMS

class LTEBaseStation:
    bsID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    pTx: int    # Transmission Power in watt
    SINR=None

    user_list = np.array([])  # List of users associated with this BaseStation. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    t_user_list = np.array([])
    lusscount = None
    lusscount2 = None
    format = None
    has_zero = None

    bits_per_symbol_of_user = dict()   # stores users and the corresponding bit value used in the symbols of PRB

    

class WifiBaseStation:
    bsID: int
    x: int  # x-coordinate
    y: int  # y-coordinate
    pTx: int    # Transmission Power in watt

    user_list = np.array([])  # List of users associated with this BaseStation. Exploiting Python's feature to assign objects to variables, thus avoiding Circular Dependency between BS and UE
    t_user_list = np.array([])
    wusscount = None
    SNR=None
    format = None
    
    bits_per_symbol_of_user = dict()   # stores users and the corresponding bit value given by MCS Table
    
