import socket
import threading
import os
import time
import subprocess
import sys
import cv2 as cv
import base64
import numpy as np
import queue

global port
port = 9999
global host
global deimos
global vidPort
vidPort= 9998


def init():
    command_thread = threading.Thread(target=command)
    receive_thread = threading.Thread(target=receive)
    command_thread.start()
    receive_thread.start()
    connectionDirection()

def command():
        while True:
            try:
                msg = input()
                handleLocal(msg)
            except:
                time.sleep(1)



def receive():
    while True:
        try:
            message = deimos.recv(4096).decode('ascii')
            if(message != ''):
                handleForeign(message)
        except:
            time.sleep(5)


def handleLocal(handled):
    if(handled == "video"):
        vidRcv()


def handleForeign(handled):
    print(handled)


def connectionDirection():
    global curState
    global host
    curState = 'connectionDirection'
    print('Enter 1 to connect to self')
    chooser = input()
    if(chooser =='1'):
        host = socket.gethostbyname(socket.gethostname())
        conn()
    else:
        hostPretender = input('Enter server ip to connect, or ''stop'' to change connection direction')
        if(hostPretender == 'stop'):
            connectionDirection()
        else:
            host = hostPretender
            conn()

def conn():



    global curState
    global deimos
    global host
    curState = 'connecting'
    try:
        deimos = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
        deimos.connect((host, port))
        print('Connected')
        vidRcv()
    except Exception as e:
        print (e)
        print('Reconnecting... ')
        time.sleep(1)
        connectionDirection()




def vidRcv():
    global q
    q = queue.Queue(maxsize=200)
    global buffer
    buffer = 999999
    def conn():
        try:
            global sock
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host,port))
            print("connected")
            global fps
            fps = float(sock.recv(4096).decode('ascii'))
            print(fps)
            rcv_thd = threading.Thread(target=receive)
            global play_thd
            play_thd = threading.Thread(target=play)
            rcv_thd.start()
        except Exception as e:
            print(e)
            conn()


    def receive():
        
        play_thd.start()
        while True:
            truther = q.full()
            if(True):
                try:
                    packet,_ = sock.recvfrom(buffer)
                    data = base64.b64decode(packet,' /')
                    npdata = np.frombuffer(data,dtype=np.uint8)

                    frame = cv.imdecode(npdata,1)
                    frame = cv.putText(frame,'FPS: '+str(fps),(10,40),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                    q.put(frame)
                    print(q.qsize())
                except Exception as e:
                    print(e)


    def play():
        while(True):
            cv.namedWindow("receive")
            cv.moveWindow('receive', 10, 360)
            teller = q.empty()
            if(teller==False):         
                cv.imshow("receive",q.get())
                key = cv.waitKey(int(1/fps*1000))
                if key == ord('q'):
                        os._exit(1)
                        TS=False
                        break
                        


    conn()