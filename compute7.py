import numpy as np
import pandas as pd
import math
import sys

import os

# Get the current file's directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two directories behind
two_dirs_behind = os.path.abspath(os.path.join(current_dir, ".."))

if os.name == "posix":
    scenename = "/" + str(os.path.abspath(os.path.join(current_dir))).split("/")[-1]
else:
    scenename = "\\" + str(os.path.abspath(os.path.join(current_dir))).split("\\")[-1]

excelpath = two_dirs_behind + scenename + "-avg.xlsx"
csvpath = two_dirs_behind + scenename + ".csv"

# print(two_dirs_behind)
# print(scenename)
print(excelpath)

data = pd.read_excel(excelpath)

timesn = int(sys.argv[1])

data = pd.read_excel(excelpath)

data[0][31] = data[0][0] /(timesn*10000)
data[0][32] = data[0][1] /(timesn*5000)

data[0][33] = data[0][2] /(timesn*10000)
data[0][34] = data[0][3] /(timesn*5000)

data[0][35] = data[0][4] /(timesn*10000)
data[0][36] = data[0][5] /(timesn*5000)

data[0][37] = data[0][6] /(timesn*10000)
data[0][38] = data[0][7] /(timesn*5000)

data[0][39] = data[0][8] /(timesn*10000)
data[0][40] = data[0][9] /(timesn*5000)

data[0][41] = data[0][10] /(timesn*10000)
data[0][42] = data[0][11] /(timesn*5000)

data[0][43] = data[0][12] /(timesn*10000)
data[0][44] = data[0][13] /(timesn*5000)

data[0][45] = data[0][14] /(timesn*10000)
data[0][46] = data[0][15] /(timesn*5000)

data[0][47] = data[0][16] /(timesn*10000)
data[0][48] = data[0][17] /(timesn*5000)




#Brute force

data[0][51] = data[0][20] /timesn

data[0][52] = data[0][21]/timesn

data[0][53] = data[0][22]/timesn

data[0][54] = data[0][23]/timesn

data[0][55] = data[0][24]/timesn

data[0][56] = data[0][25]/timesn

data[0][57] = data[0][26]/timesn

data[0][58] = data[0][27]/timesn

data[0][59] = data[0][28]/timesn


data.to_excel(excelpath,index=False)