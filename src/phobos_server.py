# https://youtu.be/YwWfKitB8aA
import socket
import threading
import os
import time
import subprocess


deimos = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #utworzenie obiektu socket z użyciem konstruktora socket (do użycia z internetem AF_INET, z protokołem TCP - sock_stream)
#host = socket.gethostbyname(socket.gethostname())
port = 11111
host = "192.168.1.31"


def kill_process_using_port(port):
    pid = subprocess.run(
        ['lsof', '-t', f'-i:{port}'], text=True, capture_output=True
    ).stdout.strip()
    if pid:
        if subprocess.run(['kill', '-TERM', pid]).returncode != 0:
            subprocess.run(['kill', '-KILL', pid], check=True)
        time.sleep(1)  # Give OS time to free up the PORT usage

def conn():
    try:
        deimos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 11111
        host = "192.168.1.31"
        deimos.connect((host, port))
        print('Connected')
    except:
        print('Reconnecting... ')
        time.sleep(3)
        conn()



def init():
    conn()
    handle_thread = threading.Thread(target=handle)
    sendMessage_thread = threading.Thread(target=sendMessage)
    handle_thread.start()
    sendMessage_thread.start()

def handle():
    while True:
        try:
            message = deimos.recv(1024).decode('ascii')
            if(message != ""):
                if str(message) == "quit":
                    print('nowIrest')
                    command("quit")
                    deimos.close()
                elif(str(message) == 1):
                    #deimosChat()
                    print("msg")
                elif(str(message) == 2):
                    print("file")
                    #deimosFile()
                elif(str(message) == 3):
                    print("vid")
                    #deimosVid()
                else:
                    print(message)
            if(message == ""):
                print('Awaiting orders ')
        except:
            time.sleep(5)
            conn()


def sendMessage():
    while True:
        try:
            msg = input()
            deimos.send(msg.encode('ascii'))
        except:
            print("Broken pipe ?")

def command(keyword):
        msg = str(keyword)
        deimos.send(msg.encode('ascii'))







