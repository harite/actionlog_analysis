#! /usr/bin/python3
import sys, getopt, string, signal
import os, re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

#########################################
# Handle command line arguments
#
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#
def help_message():
    print ('''Usage: usercount [OPTION] filename
Options:
       -h      -- displays this help message
       -s      -- specify a single school using its id
       -v      -- displays Python version''')
    sys.exit(0)
#
def split_line(text):
    timestamp, params = text.strip().split( ' - ')
    #indexes = (1,3,5,7,)
    values = params.split(' ')
    #for i in indexes:
    #    print(values[i])
    action_vars={'usertype': values[1],
                'action': values[3],
                'schoolid': values[5],
                'userid': values[7],
                'logdate': timestamp[1:11]
                }

    return action_vars

###############################################
#
#

limit_schoolid = ""
schoolid = -1
#userid = -1
#action = ""
#usertype = ""

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

dates = pd.date_range('2015-09-01', '2016-02-01', freq='D')
weeks = pd.date_range('2015-09-01', '2016-02-07', freq='W')
student_hit_series = pd.Series(0, dates)
teacher_hit_series = pd.Series(0, dates)
guardian_hit_series = pd.Series(0, dates)
student_active_series = pd.Series(0, dates)
teacher_active_series = pd.Series(0, dates)
guardian_active_series = pd.Series(0, dates)


#
student_daily_active = {datetime.strftime(i,"%Y-%m-%d"):[] for i in dates}
teacher_daily_active = {datetime.strftime(i,"%Y-%m-%d"):[] for i in dates}
guardian_daily_active = {datetime.strftime(i,"%Y-%m-%d"):[] for i in dates}

for line in log_lines:

    if re.search('SCHOOL: 101 ',line) != None or re.search('SCHOOL: 1 ',line) != None:
        continue
    if limit_schoolid!='' and re.search('SCHOOL: ' + limit_schoolid+' ', line) == None:
        continue

    action_vars = split_line(line)

    logdate=action_vars['logdate']

    if action_vars['usertype'] == 'student':
        student_hit_series[logdate] += 1
        if not(action_vars['userid'] in student_daily_active[logdate]):
            student_daily_active[logdate].append(action_vars['userid'])
            student_active_series[logdate] +=1

    elif action_vars['usertype'] == 'teacher':
        teacher_hit_series[logdate] += 1
        if not(action_vars['userid'] in teacher_daily_active[logdate]):
            teacher_daily_active[logdate].append(action_vars['userid'])
            teacher_active_series[logdate] +=1

    elif action_vars['usertype'] == 'guardian':
        guardian_hit_series[logdate] += 1
        if not(action_vars['userid'] in guardian_daily_active[logdate]):
            guardian_daily_active[logdate].append(action_vars['userid'])
            guardian_active_series[logdate] +=1


weekly_hits_frame = pd.DataFrame({'teacher':teacher_hit_series.resample('W',how=sum),
        'student':student_hit_series.resample('W',how=sum),
        'guardian':guardian_hit_series.resample('W',how=sum)})

weekly_active_frame = pd.DataFrame({'teacher':teacher_active_series.resample('W',how='mean'),
        'student':student_active_series.resample('W',how='mean'),
        'guardian':guardian_active_series.resample('W',how='mean')})

f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6), sharex=True)

#sns.set(style="darkgrid")

sns.barplot(weekly_hits_frame.index,weekly_hits_frame['teacher'],ax=ax1)
ax1.set_ylabel("Teachers")

sns.barplot(weekly_hits_frame.index,weekly_hits_frame['student'],ax=ax2)
ax2.set_ylabel("Students")

sns.barplot(weekly_hits_frame.index,weekly_hits_frame['guardian'],ax=ax3)
ax3.set_ylabel("Parents")

sns.despine(bottom=True)
plt.setp(f.axes, yticks=[], xticks=[])
plt.tight_layout(h_pad=3)
plt.show()

#print(weekly_hits_frame.resample('M',how=sum))
