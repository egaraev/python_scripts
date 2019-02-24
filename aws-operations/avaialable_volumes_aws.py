#!/usr/bin/python
#Checking avaialable EBS Volumes

from contextlib import contextmanager
import sys, os
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
import pip
required_pkgs = ['boto3', 'aws', 'awscli']
installed_pkgs = [pkg.key for pkg in pip.get_installed_distributions()]

for package in required_pkgs:
    if package not in installed_pkgs:
        with suppress_stdout():
            pip.main(['install', package])


from boto3 import Session
from csv import DictWriter

session = Session(region_name = 'eu-central-1')

def getAvailableVolumes():
    response = session.client('ec2').describe_volumes()

    availablevols = []
    for vol in response['Volumes']:
        if vol['State'] == 'available':
            availablevols.append(vol)

    with open('AvailableVolumes.csv', 'wb') as fileHandler:
        for vol in availablevols:
            if len(vol) == max([len(i) for i in availablevols]):
                fieldNames  = vol.keys()
                break
        writer = DictWriter(fileHandler, fieldnames=fieldNames)
        writer.writeheader()
        for vol in availablevols:
            writer.writerow(aVol)

try:
    getAvailableVolumes()
except Exception as ex:
    print "Exception Occurred: %s"%(ex)