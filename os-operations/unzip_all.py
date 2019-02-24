#!/usr/bin/python
#script for unziping all files in some directory

import zipfile
from os import listdir
from os.path import isfile, join
directory = "/home/eldar/archives/"
onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
for o in onlyfiles:
    if o.endswith(".zip"):
        print(directory+o)
        with zipfile.ZipFile(directory+o,"r") as zip_ref:
            zip_ref.extractall("/home/eldar/archives/unziped/")