import os
import tempfile

cwd = os.getcwd()
print(cwd)

newdir = os.path.join(cwd, "ML")

if not os.path.exists(newdir):
    os.mkdir(newdir)

print(os.listdir(cwd))
cwd = os.chdir(newdir)

newdir = os.path.join(newdir, "luty_26")

if not os.path.exists(newdir):
    os.mkdir(newdir)
    
print(os.listdir(cwd))
cwd = os.chdir(newdir)

newfile = os.path.join(newdir, "dummy_file.txt")
lines = ["Hey hey hey", "Beep beep", "I see that I'm icy", "Go rising up", "I see that I'm icy"]

with open(newfile, "w") as mf:
    for line in lines:
        mf.write(line + "\n")
    with open("..\..\os.py", "r") as script:
        for l in script.readlines():
            mf.write(l)

with open(newfile, "r") as f:
    for line in f.readlines():
        print(line)
        