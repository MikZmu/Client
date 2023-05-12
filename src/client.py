import socket
import time
import pickle
import threading
import cv2 as cv
import base64
import queue
import numpy as np
global q
q = queue.Queue(maxsize=200)
global buffer
buffer = 999999999
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
location = 'ANY'

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






def connectionDirection():
    global host
    while(True):
        clear()
        print('1 : connect to self')
        print('2 : connect to other')
        chooser = input()
        if(chooser == '1'):
           host = socket.gethostbyname(socket.gethostname())
           return 1
        if(chooser == '2'):
            host = input("enter server ip: ")
            return 2
    


def interface():
    global connState
    global table
    isLinux()
    while(True):
        #clear()
        print("Connection: "+" :: "+ connState)
        if(state == 'connection menu' and connState == 'disconnected'):
            print('1 : connection setup')
            print('2 : connect')
            command = input()
            handle(command)
        if(state == 'connection menu' and connState == 'connected'):
            print('1 : connection setup')
            print('2 : connect')
            print("3 : browse")
            command = input()
            handle(command)
        if(state == 'browse'):
            print('1 : connection setup')
            print('2 : connect')
            print("3 : menu")
            print(f"Start Time: {startTime} :: End Time: {endTime}  :: Location: {location}")
            print("StartTime to set start time")
            print("EndTime to set end time")
            print("Location to set location")
            print("enter ANY to search for any")
            print("Play [id] to play video")
            command = input()
            handle(command)


def handle(command):
    global state
    global startTime
    global endTime
    global location
    if(state == 'connection menu' and connState == 'disconnected'):
        if(command=='1'):
            connectionDirection()
        if(command=='2'):
            connectionToggle()
    if(state == 'connection menu' and connState == 'connected'):
        if(command=='1'):
            connectionDirection()
        if(command=='2'):
            connectionToggle()
        if(command=='3'):
            state = 'browse'
    if(state == 'browse'):
        if(command == '1'):
            connectionDirection()
        if(command =='2'):
            connection()
        if(command == '3'):
            state == 'connection menu'
        if(command == 'StartTime'):
            startTime = input("YYYY-MM-DD HH:MM:SS : ")
            request(location, startTime, endTime)
        if(command == 'EndTime'):
            endTime = input("YYYY-MM-DD HH:MM:SS : ")
            request(location, startTime, endTime)
        if(command == 'location'):
            location = input("location: ")
            request(location, startTime, endTime)
        if(command =='play'):
            id = input('ID: ')
            rcvStr(id)

def rcvStr(id):
    global fps
    server.send(f'play&{id}'.encode('ascii'))
    fps = float(sock.recv(4096).decode('ascii'))
    rcv_thd = threading.Thread(target=receive)
    global play_thd
    play_thd = threading.Thread(target=play)
    rcv_thd.start()
        
def receive():
        play_thd = threading.Thread(target=play)
        play_thd.start()
        while True:
            if(True):
                try:
                    packet,_ = sock.recvfrom(buffer)
                    data = base64.b64decode(packet,' /')
                    npdata = np.frombuffer(data,dtype=np.uint8)

                    frame = cv.imdecode(npdata,1)
                    frame = cv.putText(frame,'FPS: '+str(fps),(10,40),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                    q.put(frame)

                except Exception as e:
                    print(e)


def play():
    while(True):
        cv.namedWindow("receive")
        cv.moveWindow('receive', 10, 360)
        teller = q.empty()
        print(q.qsize())
        fpsInt = int(fps)
        keyy = int((1/fpsInt) * 1000)
        if(teller==False):         
            cv.imshow("receive",q.get())
            key = cv.waitKey(keyy)
            if key & 0xFF== ord('q'):
                    break

    

def request(location, startTime, endTime):
    global table
    server.send(f'request&{location}&{startTime}&{endTime}'.encode('ascii'))
    arr = server.recv(4096)
    table = pickle.loads(arr)
    for row in table:
        print ("Id = ", row[0], "Location = ", row[1], "Time= ", row[2])
    
    


def connectionToggle():
    global toggle
    if(toggle == False):
        toggle = True
        #connThread.start()
        connection(toggle, stream)
    else:
        toggle = False
        connection(toggle, stream)

def connection(toggle, stream):
    global server
    global sock
    global connState
    if(toggle == True):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((host, 9999))
            print('Connected to server')
            global sock
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host,9999))
            print("connected to video")
            connState = 'connected'
        except Exception as e:
            connState = 'disconnected'
            print (e)
            print('Reconnecting... ')
            time.sleep(5)


#def receive():



interface()

