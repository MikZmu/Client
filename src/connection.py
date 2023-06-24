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
        #clear()
    print('1 : connect to self')
    print('2 : connect to other')
    chooser = input()
    if(chooser == '1'):
        host = socket.gethostbyname(socket.gethostname())
    if(chooser == '2'):
        host = input("enter server ip: ")

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
    global connState
    global fps
    try:
        server.send(f'play&{id}'.encode('ascii'))
    except Exception as e:
            connState = str(e)
    receivendplay()

def receivendplay():


    global connState
    #fps = float(sock.recv(4096).decode('ascii'))
    try:
        fps = float(server.recv(1024).decode('ascii'))
        secondPart = server.recv(1024).decode('ascii')
        capture =  cv.VideoCapture(f"http://{host}:{secondPart}/stream.mjpg")
    except:
        connState = 'disconnected'
    #fpsInt = int(fps)
    #keyy = int((1/fpsInt) * 1000)


    while(True):
        try:
            _, frame = capture.read()
            cv.imshow('stream', frame)
            if cv.waitKey(int(1000/fps))==ord("q"):
                server.send('stop'.encode('ascii'))
                break 
        except Exception as e:
            print(str(e))
            try:
                server.send('stop'.encode('ascii'))
            except:
                connState = 'disconnected'
            break
        
    try:
        capture.release()
        cv.destroyAllWindows()
    except Exception as e:
        print(e)

def request(location, startTime, endTime):
    global connState
    global table
    try:
        server.send(f'request&{location}&{startTime}&{endTime}'.encode('ascii'))
        arr = server.recv(4096)
        table = pickle.loads(arr)
        return table
    except:
        connState = 'disconnected'

def connection():
    global server
    global sock
    global connState
    global vidConn
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(True):
        time.sleep(1)
        try:
            if(connState != 'connected'):
                server.connect((host, 9999))                                                    
                connState = 'connected'
        except Exception as e:
            connState = str(e)
            time.sleep(5)
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    
