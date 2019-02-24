#!/usr/bin/python
from __future__ import print_function, unicode_literals

# Netmiko is the same as ConnectHandler
from netmiko import Netmiko
from getpass import getpass

passwd = getpass()

cisco1 = {
    "host": "192.168.0.1",
    "username": "admin",
    "password": passwd,
    "device_type": "cisco_ios",
}

cisco2 = {
    "host": "192.168.1.1",
    "username": "cisco",
    "password": passwd,
    "device_type": "cisco_ios",
}

cisco3 = {
    "host": "192.168.3.1",
    "username": "root",
    "password": passwd,
    "device_type": "cisco_ios",
}


def append_doc(file_name, varable):
	f=open(file_name, 'a')
	f.write(varable)
	f.write('\n')
	f.close()
	

def write_doc(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()

file_name = "results.csv"
write_doc(file_name, "")

for router in (cisco1, cisco2, cisco3):
    net_connect = Netmiko(**router)
    print(net_connect.find_prompt())
    output = net_connect.send_command_expect('show ver | i .bin')
    for each_word in output.split(" "):
		if ".bin" in each_word:
		    ver = each_word
    results = router + "," + ver
    append_doc(file_name, results)