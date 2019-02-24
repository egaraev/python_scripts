#!/usr/bin/python
#Very simple example how to resolve name to ip using python
import os
import re
domain = os.popen("host www.google.com")
re_dns = re.compile(r"([\d]+)\.([\d]+)\.([\d]+)\.([\d]+)")
for line in domain.readlines():
  hst=re_dns.search(line)
  if (hst != None):
    break
host=hst.group(0)
print "Google host adress is "+host