# https://youtu.be/YwWfKitB8aA
import socket
import threading
import os
import time
import subprocess
import sys


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
    chooser = input('Enter 1 to connect to self')
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
    except:
        print('Reconnecting... ')
        time.sleep(5)
        conn()

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
                print(message)
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







