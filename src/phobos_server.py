# https://youtu.be/YwWfKitB8aA
import socket
import threading
import os
import time
import subprocess
import sys
import cv2
import base64
import numpy as np

global port
port = 9999
global host
global deimos
global curState


def kill_process_using_port(port):
    try:
        pid = subprocess.run(
            ['lsof', '-t', f'-i:{port}'], text=True, capture_output=True
        ).stdout.strip()
        if pid:
            if subprocess.run(['kill', '-TERM', pid]).returncode != 0:
                subprocess.run(['kill', '-KILL', pid], check=True)
            time.sleep(1)  # Give OS time to free up the PORT usage'''
    except:
        print("Maybe it is not Linux ???")

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
        #host = '192.168.0.27'
        deimos.connect((host, port))
        print('Connected')
    except Exception as e:
        print (e)
        print('Reconnecting... ')
        time.sleep(5)
        connectionDirection()

def isLinux():
    global curState
    curState = 'isLinux'
    print("Enter 1 if program runs on Linux: ")
    isLin = input()
    global linuxMode
    if(isLin == '1'):
        linuxMode = 1
    else:
        linuxMode = 0
    connectionDirection()

def init():
    command_thread = threading.Thread(target=command)
    receive_thread = threading.Thread(target=receive)
    command_thread.start()
    receive_thread.start()
    connectionDirection() 
    
def communicationBreakdown():
    global curState
    curState = 'communicationBreakdown'
    try:
        deimos.close()
    except:
        print('attempting to close connection ...')
        communicationBreakdown()

def handle(handled): 
        if handled == "stop":
            if(curState == 'connecting' or curState == 'binding'):
                isLinux()
            elif(curState == 'connected' or curState =='streaming'):
                communicationBreakdown()
                isLinux()
            elif(curState == 'isLinux' or curState == 'quitPrompt'):
                quitPrompt()
                isLinux()
        elif(handled == 'browse'):
            #browse()
            print("waiting For Browse function")
        elif(handled == 'film'):
            rcvVid()
        else:
            print(handled)

def quitPrompt():
    global curState
    curState = 'quitPrompt'
    chooser = input('Enter ''stop'' to terminate')
    if(chooser =='stop'):
        print('goodbye')
        sys.exit()


def receive():
    while True:
        try:
            message = deimos.recv(4096).decode('ascii')
            if(message != ''):
                handle(message)
            #if(message != ''):
            #    handle(message)
        except:
            time.sleep(5)
            if(curState == 'connected'):
                print('OMG CONNECTION LOST -> TRYING TO RECONNECT')
                conn()



def command():
        while True:
            try:
                msg = input()
                deimos.send(msg.encode('ascii'))
            except:
                time.sleep(1)



def rcvVid():
    vidPort = 9998
    buffer = 65536
    

    """def connVid():
        global deimosVid
        try:
            deimosVid = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
            deimos.connect((host, vidPort))
            print('Connected Video')
        except Exception as e:
            print(e)
            print('Reconnecting Video ')
            time.sleep(5)
            connVid()"""

    def rcv():
        cv2.namedWindow('RECEIVING VIDEO')        
        cv2.moveWindow('RECEIVING VIDEO', 10,360) 
        fps,st,frames_to_count,cnt = (0,0,2000,0)
        while True:
            packet,_ = deimos.recvfrom(buffer)
            data = base64.b64decode(packet,' /')
            npdata = np.fromstring(data,dtype=np.uint8)

            frame = cv2.imdecode(npdata,1)
            frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                
                os._exit(1)
                break

            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-st),1)
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1

    #connVid()
    rcv()



