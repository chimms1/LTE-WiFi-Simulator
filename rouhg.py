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

print(two_dirs_behind)
print(scenename)
print(excelpath)

# # Get the current file's directory path
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # Go two directories behind


# print(scenename)