#! /usr/bin/python3
import sys, getopt, string, signal
import os, re

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
       -d      -- specify the directory (it expects an argument)
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
    
    return userid, action

###############################################
#
hit_counts = {'student': 0, 'teacher':0, 'guardian':0}
students = {}
teachers = {}
guardians = {}
teacher_homeworks = {}
teacher_resources = {}
teacher_topiclines = {}
teacher_reviews = {}

limit_schoolid = ""
schoolid = -1
userid = -1
action = ""
usertype = ""

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



###############################################
#
for filename in args[:]:
    try:
        logfile = open(filename, 'r')
        print ("Reading... ", filename)
        for line in logfile:
            
            if re.search('SCHOOL: 101 ',line) != None or re.search('SCHOOL: 1 ',line) != None:
                continue
            if limit_schoolid!='' and re.search('SCHOOL: ' + limit_schoolid+' ', line) == None:
                continue

            
            if re.search('USER: student',line) != None:
                userid, action = split_line(line)
                #print(userid,"did this",action)
                hit_counts['student'] += 1
                if userid in students:
                    students[userid] += 1
                else:
                    students[userid] = 1
                    
            elif re.search('USER: teacher',line) != None:
                userid, action = split_line(line)
                #print(userid,"did this",action)
                hit_counts['teacher'] += 1
                if userid in teachers:
                    teachers[userid] += 1
                else:
                    teachers[userid] = 1

                if action == 'teacher/createHomework':
                    if userid in teacher_homeworks:
                        teacher_homeworks[userid] += 1
                    else:
                        teacher_homeworks[userid] = 1
                elif re.search('homework/review',action) != None:
                    if userid in teacher_reviews:
                        teacher_reviews[userid] += 1
                    else:
                        teacher_reviews[userid] = 1
                elif action == 'resources/new':
                    if userid in teacher_resources:
                        teacher_resources[userid] += 1
                    else:
                        teacher_resources[userid] = 1
                elif action == 'resources/topicLine':
                    if userid in teacher_topiclines:
                        teacher_topiclines[userid] += 1
                    else:
                        teacher_topiclines[userid] = 1
                    

                
            elif re.search('USER: guardian',line) != None:
                userid, action = split_line(line)
                #print(userid,"did this",action)
                hit_counts['guardian'] += 1
                if userid in guardians:
                    guardians[userid] += 1
                else:
                    guardians[userid] = 1
                        
        logfile.close()
    except IOError as e:
        print("Can't open file:", filename)


#
#
print("--")
print("Students =",len(students))
print("Student hits =",hit_counts['student'])
print("--")
print("Parents =",len(guardians))
print("Parent hits =",hit_counts['guardian'])
print("--")
print("Teachers =",len(teachers))
print("Teacher hits =",hit_counts['teacher'])
print("Teacher homework users =",len(teacher_homeworks))
print("Teacher reviews homework users =",len(teacher_reviews))
print("Teacher resource users =",len(teacher_resources))
print("Teacher topicline users =",len(teacher_topiclines))

super_teachers = 0
for userid in teacher_homeworks.keys():
    if userid in teacher_topiclines and teacher_topiclines[userid]>4 and teacher_homeworks[userid]>10:
        super_teachers += 1
        print(userid)
        
print("")
print("Super Teachers! Doing both homework and topiclines ", super_teachers)
