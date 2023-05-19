import socket
import pickle
import cv2 as cv
import time
import os
import threading
import base64
import numpy as np
import queue
global q
q = queue.Queue(maxsize=200)
global buffer
buffer = 999999999
global toggle
toggle = False
global host
host = socket.gethostbyname(socket.gethostname())
global connState
global vidConn
connState = 'disconnected'
vidConn = 'disconnected'






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
        
def clear():
    if(linuxMode == 1):
        clear = lambda: os.system('clear')
        clear()
    else:
        clear = lambda: os.system('cls')
        clear()

def isLinux():
    print("IsLinux")
    from sys import platform
    global linuxMode
    if(platform == "linux" or platform == 'linux2'):    
        linuxMode = 1   
    else:
        linuxMode = 0

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
        keyy = int((1/fpsInt) * 500)
        if(teller==False):         
            cv.imshow("receive",q.get())
            key = cv.waitKey(keyy)
            if key & 0xFF== ord('q'):
                    break

def connectionToggle():
    global toggle
    if(toggle == False):
        toggle = True
    else:
        toggle = False

def request(location, startTime, endTime):
    global table
    server.send(f'request&{location}&{startTime}&{endTime}'.encode('ascii'))
    arr = server.recv(4096)
    table = pickle.loads(arr)
    return table

def connection():
    global server
    global sock
    global connState
    global vidConn
    global alarmTab
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(True):
        try:
            if(connState != 'connected'):
                server.connect((host, 9999))
                connState = 'connected'
        except Exception as e:
            connState = str(e)
            time.sleep(5)
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if(vidConn != 'connected'):
                sock.connect((host,9999))
                vidConn = 'connected'
        except Exception as e:
            vidConn = str(e)
            time.sleep(5)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def getConnState():
    try:
        return connState
    except:
        return 'disconnected'

def getvidConn():
    try:
        return vidConn
    except:
        return 'disconnected'