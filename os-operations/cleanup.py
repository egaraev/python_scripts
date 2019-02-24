#!/usr/bin/python
#Script for cleaning empty directories and old files
import os
import time

days = 1   #Maximum age of file to stay. Older files will be removed
folders = [
            "/data/app",
            "/data_log/logs",
            "/tmp/db_logs"
          ]
total_removed_size = 0
total_removed_file = 0
total_removed_dirs = 0

currenttime = time.time()  #get current time in seconds
agetime = currenttime-60*60*24*days

def remove_old_files(folder):
    #remove files older than few days
    global total_removed_file
    global total_removed_size
    for path, dirs, files in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)  #get full path to file
            filetime = os.path.getmtime(filename)
            if filetime < agetime:
                sizefile = os.path.getsize(filename)
                total_removed_size += sizefile
                total_removed_file += 1
                print("Removing file " + str(filename))
                os.remove(filename)


def remove_empty_dir(folder):
    global total_removed_dirs
    empty_folders_current_run = 0
    for path, dirs, files in os.walk(folder):
        if (not dirs) and (not files):
            total_removed_dirs += 1
            empty_folders_current_run += 1
            print("Removing empty directory: " + str(path))
            os.rmdir(path)
    if empty_folders_current_run>0:
        remove_empty_dir(folder)


starttime=time.asctime()

for folder in folders:
    remove_old_files(folder)     #removing old files
    remove_empty_dir(folder)    #deleting empty folders


finishtime = time.asctime()

print ("###################################################")
print ("Start time: " + str(starttime))
print ("Total removed size: " +str(total_removed_size/1024/1024) + "MB")
print ("Total removed files: " + str(total_removed_file))
print ("Total removed folders: " + str(total_removed_dirs))
print ("Finish time: "  + str(finishtime))


