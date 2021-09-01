from flask import Flask, render_template, request
from file_read_backwards import FileReadBackwards
import os
import csv 
from pathlib import Path
import  pandas as pd
import numpy as np
from datetime import datetime

class sum_data:
     
    def __init__(self, _avg_down_speed,_avg_up_speed, _avg_ping,_min_down_speed, _max_down_speed, _min_up_speed, _max_up_speed, _min_ping, _max_ping):
        self.avg_down_speed = _avg_down_speed
        self.avg_up_speed = _avg_up_speed
        self.max_down_speed = _max_down_speed
        self.max_up_speed = _max_up_speed
        self.min_down_speed = _min_down_speed
        self.min_up_speed = _min_up_speed
        self.avg_ping = _avg_ping
        self.min_ping = _min_ping
        self.max_ping = _max_ping

class file_data:
    def __init__(self, _name):
        self.name = _name

class log_data:
    def __init__(self, _id, _date, downspeed, upspeed, _ping):
        self.id = _id
        self.date = _date
        self.down = downspeed
        self.up = upspeed
        self.ping=_ping
    def __lt__(self,other):
        return self.id <  other.id
    def __gt__(self,other):
        return self.id > other.id
 
app = Flask(__name__, template_folder='.')

data = []

def read_csv(csvfile):
    counter = 0
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
          counter +=1
          data_log_item = log_data(counter, row[0], row[1], row[2], row[3])
          data.append(data_log_item)

def getFileList(path):
    result = []
    p = Path(path)
    for name in p.glob('speedtest.*'):
        itemdata = file_data(name)
        result.append(itemdata)
        #print(name)
    return result

def generate_summary(path):
    df =pd.read_csv(path, names=['date','down','up','ping'])
    #df['down'] = df['down'].map(lambda x: x.lstrip('MB').rstrip('MB'))
    df['down'] = df['down'].str.replace('MB','') 
  #  df['up'].map(lambda x: x.lstrip('Mb').rstrip('Mb'))
    df['up'] = df['up'].str.replace('Mb','') 
#    df['ping'] = df['ping'].map(lambda x: x.lstrip('ms').rstrip('ms'))
    df['ping'] = df['ping'].str.replace('ms','')
    df["down"] = pd.to_numeric(df["down"], downcast="float")
    df["up"] = pd.to_numeric(df["up"], downcast="float")
    df["ping"] = pd.to_numeric(df["ping"], downcast="float")

    avg_down_speed =df['down'].mean()
    avg_up_speed =df['up'].mean()
    avg_ping=df['ping'].mean()
    min_down_speed =df['down'].min()
    max_down_speed=df['down'].max()
    min_up_speed=df['up'].min()
    max_up_speed=df['up'].max()
    min_ping =df['ping'].min()
    max_ping=df['ping'].max()
    result = []
    item = sum_data(avg_down_speed, avg_up_speed, avg_ping, min_down_speed, max_down_speed, min_up_speed, max_up_speed,  min_ping, max_ping)
    result.append(item)
    #print(df.head())
    return result

@app.route("/", methods=['GET', 'POST'])
def speedTest():
    filename1 ="/var/log/speedtest.log"
    filename1 = filename1 + '-' + datetime.strftime(datetime.now(),'%Y%m%d')
    data.clear()  
    old_files =[]
    summary = []
    if request.method == 'POST':
        filename = request.form.get('open')
        #print(filename)
    elif request.method == 'GET':
        filename =filename1#'/var/log/speedtest.log'
    else:
        filename =filename1#'/var/log/speedtest.log'

    #read_csv('/var/log/speedtest.log')
    read_csv(filename)
    old_files = getFileList('/var/log/')
    data.sort(reverse=True)
    summary = generate_summary(filename)
    #print(len(old_files))
    return  render_template('logview.html', summary=summary,old_files=old_files, data=data)



