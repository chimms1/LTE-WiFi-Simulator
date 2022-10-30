# Create and display graphs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

wussdf = pd.read_csv("wussdf.csv")
lussdf = pd.read_csv("lussdf.csv")
wbssdf = pd.read_csv("wbssdf.csv")
lbssdf = pd.read_csv("lbssdf.csv")

x1 = lussdf.iloc[:, 0:1]
y1 = lussdf.iloc[:, 1:2]

x2 = wussdf.iloc[:, 0:1]
y2 = wussdf.iloc[:, 1:2]

x3 = lbssdf.iloc[:, 0:1]
y3 = lbssdf.iloc[:, 1:2]

x4 = wbssdf.iloc[:, 0:1]
y4 = wbssdf.iloc[:, 1:2]

plt.scatter(x1, y1, marker='x', color='red')
plt.scatter(x2, y2, marker='x', color='blue')
plt.scatter(x3, y3, marker='^', color='red', s=100)
plt.scatter(x4, y4, marker='^', color='blue', s=100)
plt.legend(["LTE User", "Wi-Fi User", "LTE BS", "Wi-Fi BS"])
plt.xlim(0, 100)
plt.ylim(0, 100)

# Create and display graphs
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

wussdf = pd.read_csv("wussdf.csv")
lussdf = pd.read_csv("lussdf.csv")
wbssdf = pd.read_csv("wbssdf.csv")
lbssdf = pd.read_csv("lbssdf.csv")

x1 = lussdf.iloc[:, 0:1]
y1 = lussdf.iloc[:, 1:2]

x2 = wussdf.iloc[:, 0:1]
y2 = wussdf.iloc[:, 1:2]

x3 = lbssdf.iloc[:, 0:1]
y3 = lbssdf.iloc[:, 1:2]

x4 = wbssdf.iloc[:, 0:1]
y4 = wbssdf.iloc[:, 1:2]

plt.scatter(x1, y1, marker='x', color='red')
plt.scatter(x2, y2, marker='x', color='blue')
plt.scatter(x3, y3, marker='^', color='red', s=100)
plt.scatter(x4, y4, marker='^', color='blue', s=100)
plt.legend(["LTE User", "Wi-Fi User", "LTE BS", "Wi-Fi BS"])
plt.xlim(0, 100)
plt.ylim(0, 100)

plt.xlabel("X-Coordinates")
plt.ylabel("Y-Coordinates")
plt.title("Scene1: 1LTE BS & 1Wi-Fi BS")

plt.show()