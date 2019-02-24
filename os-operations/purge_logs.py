#!/usr/bin/python
#log rotation script. Rename old big file and clear current one
# python purge_logs.py log/messages 10 5
import sys, os
import shutil


if (len(sys.argv) < 4):
    print("Missed arguments")
    exit(1)

file_name = sys.argv[1]
limitsize = int(sys.argv[2])     #minimum size for purging in KB  
logsnumber = int(sys.argv[3])   # how many logs we can create

if (os.path.isfile(file_name) == True):
    logfile_size = os.stat(file_name).st_size
    logfile_size = logfile_size / 1024

    if (logfile_size >= limitsize):
        if(logsnumber > 0):
            for currentfilenumber in range (logsnumber, 1, -1):
                src = file_name + "_" + str(currentfilenumber-1)
                dst = file_name + "_" + str(currentfilenumber)
                if(os.path.isfile(src) == True):
                    shutil.copyfile(src, dst)
                    print("Copied: " +src + " to " + dst)
            shutil.copyfile(file_name, file_name + "_1")
            print ("Copied: " + file_name + "  to " + file_name + "_1")
        myfile=open(file_name, "w")
        myfile.close()
