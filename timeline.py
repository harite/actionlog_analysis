#! /usr/bin/python3
import sys, getopt, string, signal
import os, re
import numpy as np
import pandas as pd
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt

#
#
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#
#
def help_message():
    print ('''Usage: usercount [OPTION] filename
Options:
       -h      -- displays this help message
       -s      -- specify a single school using its id
       -v      -- displays Python version''')
    sys.exit(0)
#
#
def split_line(text):
    timestamp, params = text.strip().split( ' - ')
    indexes = (1,3,5,7,)
    values = params.split(' ')
    #for i in indexes:
    #    print(values[i])
    usertype = values[1]
    action = values[3]
    schoolid = values[5]
    userid = values[7]
    logdate = timestamp[1:11]

    return userid, action, logdate
#
#
try:
    options, args = getopt.getopt(sys.argv[1:],'hs:v', ['version'])
except getopt.error:
    print('''Nope: didn't recognise that option or you missed an argument.
    Try `-h\' for more info''')
    sys.exit(0)
for o in options[:]:
    if o[0] == '-h':
        help_message()
    elif o[0] == '-s' and o[1] != '':
        limit_schoolid = o[1]
        print('Limit results to school id ' + limit_schoolid)
        options.remove(o)
        break
    elif o[0] == '-s' and o[1] == '':
        print('-s expects a school id as an argument')
        sys.exit(0)
    elif o[0] == '-v' or o[0] == '--version':
        print('help version 0.0.001')
        print('Python '+sys.version)
        sys.exit(0)
#
#
for filename in args[:]:
    try:
        file = open(filename, 'r')
        print ("Reading... ", filename)
        log_lines = file.read().splitlines()
        file.close()
    except IOError as e:
        print("Can't open file:", filename)
        sys.exit(0)


########################################################
#
#
#

dates = pd.date_range('2015-09-16', '2015-12-14', freq='W')
hit_series = pd.Series(0, dates)

for line in log_lines:

    if re.search('SCHOOL: 101 ',line) != None or re.search('SCHOOL: 1 ',line) != None:
        continue
    if limit_schoolid!='' and re.search('SCHOOL: ' + limit_schoolid+' ', line) == None:
        continue

    userid, action, logdate = split_line(line)

    #date=pd.to_datetime('2015-10-28')
    hit_series.loc[logdate] += 1

'''
            if re.search('USER: student',line) != None:

            elif re.search('USER: teacher',line) != None:

            elif re.search('USER: guardian',line) != None:
'''


#hit_series.plot()


