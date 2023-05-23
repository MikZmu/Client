import socket
import time
import pickle
import threading
import cv2 as cv
import base64
import queue
import numpy as np
import connection
global host

global state
global server
global video
state = "connection menu"
global linuxMode
global connState
connState = 'disconnected'
import os
toggle = False
stream = False
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
                for row in result:
                    print("ID: "+str(row[0])+" Location: "+ row[1]+ " Time: " + row[2])
            except Exception as e:
                print(f"There was a problem with displaying data. Exception {e}")
            print("Command: ")
        update.clear()

def handle(command):
    global connState
    global vidConn
    global state
    global startTime
    global endTime
    global location
    global result
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
            if(command =='2'):
                connection.connection()
            if(command == '3'):
                state == 'connection menu'
            if(command =='4'):
                print("XOXO")
            if(command == 'StartTime'):
                print("YYYY-MM-DD HH:MM:SS : ")
                startTime = input()
            if(command == 'EndTime'):
                endTime = input("YYYY-MM-DD HH:MM:SS : ")
            if(command == 'location'):
                location = input("location: ")
            if(command =='play'):
                id = input('ID: ')
                connection.rcvStr(id)
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
        time.sleep(0.1)

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

