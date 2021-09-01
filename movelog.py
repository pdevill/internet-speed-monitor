#!/usr/bin/python3
from datetime import datetime
import os

log_file = "/var/log/speedtest.log"
new_filename = log_file+ '-' + datetime.strftime(datetime.now(),'%Y%m%d')



os.rename(log_file,new_filename)





