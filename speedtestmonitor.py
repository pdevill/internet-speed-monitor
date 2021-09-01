#!/usr/bin/python3

import speedtest
import os
from datetime import datetime

logfile = "/var/log/speedtest.log"
filename = logfile + '-' + datetime.strftime(datetime.now(),'%Y%m%d')

isp = speedtest.Speedtest()
srv = isp.get_best_server()
downstream = "{0:,.2f} MB".format(float(isp.download()/10**6))
upstream ="{0:,.2f} Mb".format(float(isp.upload()/10**6))
latency ="{0:,.2f} ms".format(float(srv['latency']))
update = datetime.strftime(datetime.now(),'%d/%m/%y %I:%M%p')

with open(filename,'a+') as file:
    file.write(F"{update},{downstream},{upstream},{latency}\n")

print(f"{logfile} update.")

