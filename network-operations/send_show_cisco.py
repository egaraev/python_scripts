#!/usr/bin/python
from netmiko import Netmiko
from getpass import getpass
import logging

logging.basicConfig(filename="cisco.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

cisco_device = {
    "host": "192.168.0.1",
    "username": "admin",
    "password": getpass(),
    "device_type": "cisco_ios",
}

net_connect = Netmiko(**cisco_device)
command = "show ip int brief"

print()
print(net_connect.find_prompt())
cli_output = net_connect.send_command(command)
net_connect.disconnect()
print(cli_output)
print()