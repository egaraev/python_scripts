#!/usr/bin/env python
from netmiko import Netmiko
from getpass import getpass
import logging

logging.basicConfig(filename="cisco.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")


router = {
    "host": "192.168.0.1",
    "username": "admin",
    "password": getpass(),
    "device_type": "cisco_ios",
}

commands = ["access-list 90 deny 131.108.134.234"]

network_connect = Netmiko(**router)

print()
print(network_connect.find_prompt())
output = network_connect.send_config_set(commands)
output += network_connect.send_command("copy run start")
print(output)
print()