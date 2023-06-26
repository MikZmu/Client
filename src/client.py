import time
import threading
import cv2 as cv
import numpy as np
import connection
import os
global page
page = 0
global result
global state
state = "connection menu"
global linuxMode
global connState
connState = 'disconnected'
global table
global startTime
startTime = '1900-01-01 00:00:00'
global endTime
endTime = '3000-12-31 23:25:29'
global location
location = 'atrium'

def isLinux():
    print("IsLinux")
    from sys import platform
    global linuxMode
    if(platform == "linux" or platform == 'linux2'):    
        linuxMode = 1   
    else:
        linuxMode = 0

def clear():
    if(linuxMode == 1):
        clear = lambda: os.system('clear')
        clear()
    else:
        clear = lambda: os.system('cls')
        clear()

def interface():
    global result
    while(True):
        update.wait()
        clear()
        if(state == 'connection menu'):
            print("CONNECTION :::: " + connState)
            print('1 : Connection setup :::::::::: 2 : browse')
            print("Command: ")
        elif(state == 'browse'):
            print("CONNECTION :: SERVER :: " + connState)
            print('1 : connection setup **** 2 : connect **** 3 : menu **** 4 : show state')
            print(f"Start Time: {startTime} **** End Time: {endTime}  **** Location: {location}")
            print("StartTime to set start time **** EndTime to set end time **** Location to set location **** Play to play video")
            result = connection.request(location, startTime, endTime)
            try:
                for x in range(page * 10, ((page +1)  * 10)):
                    print("ID: "+str(result[x][0])+" Location: "+ result[x][1]+ " Time: " + result[x][2])
            except Exception as e:
                print(f"There was a problem with displaying data. Exception {e}")
            print("Page: " + str(page+1) + " out of " + str(int(len(result)/10+1)))
            print("Command: ")
        update.clear()

def handle(command):
    global connState
    global state
    global startTime
    global endTime
    global location
    global result
    global page
    if(state == 'connection menu'):
        if(command=='1'):
            connection.connectionDirection()
        elif(command =='2' and connState == 'connected'):
            state = 'browse'
        elif(command == '2' and connState == 'disconnected'):
            print('Can\'t browse in offline mode !')
        elif(command == '3'):
            print("XOXO")
    elif(state == 'browse'):
        if(connState == 'connected'):
            if(command == '1'):
                connection.connectionDirection()
            elif(command =='2'):
                connection.connection()
            elif(command == '3'):
                state == 'connection menu'
            elif(command =='4'):
                print("XOXO")
            elif(command == 'StartTime'):
                print("YYYY-MM-DD HH:MM:SS : ")
                startYear = input('year ')
                startMonth = input('month ')
                startDay = input('day ')
                startHour = input('hour ')
                startMinute = input('minute ')
                startSecond = input('second ')
                startTime = startYear+'-'+startMonth+'-'+startDay+" "+startHour+":"+startMinute+":"+startSecond
            elif(command == 'EndTime'):
                print("YYYY-MM-DD HH:MM:SS : ")
                endYear = input('year ')
                endMonth = input('month ')
                endDay = input('day ')
                endHour = input('hour ')
                endMinute = input('minute ')
                endSecond = input('second ')
                endTime = endYear+'-'+endMonth+'-'+endDay+" "+endHour+":"+endMinute+":"+endSecond
            elif(command == 'location'):
                location = input("location: ")
            elif(command =='play'):
                id = input('ID: ')
                connection.rcvStr(id)
            elif(command == 'next'):
                if(page < int(len(result)/10)):
                  page += 1
            elif(command == 'prev'):
                if(page > 0):
                  page -= 1
        if(connState == 'disconnected'):
            state = 'connection menu'

def command():
    while(True):
        command = input()
        if(command != ""):
            handle(command)
            update.set()
     
def getState():
    global connState
    while(True):
        newConnState = connection.getConnState()
        if(newConnState != connState):
            connState = newConnState
            update.set()
        time.sleep(0.5)

isLinux()
update = threading.Event()
commThd = threading.Thread(target=command)
dispThd = threading.Thread(target=interface)
dispThd.start()
connection.isLinux()
connThd = threading.Thread(target=connection.connection)
connThd.start()
stateThd = threading.Thread(target=getState)
stateThd.start()
commThd.start()


