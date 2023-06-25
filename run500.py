import os
import sys

times = int(sys.argv[1])

# Get the current file's directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two directories behind
two_dirs_behind = os.path.abspath(os.path.join(current_dir))

print(two_dirs_behind)


# Give file path according to OS
if os.name == "posix":
    mainfilepath = two_dirs_behind + "/Simulator/main-latest-all.py"
else:
    mainfilepath = two_dirs_behind + "\Simulator\main-latest-all.py"

print(mainfilepath)

for i in range(times):
    print(i)
    os.system("python"+" "+str(mainfilepath)+" "+str(i))

# os.system("python compute7.py "+str(times))