import socket
import cv2 as cv
import base64
import numpy as np
import queue
import os
import threading
port = 9999
global q
q = queue.Queue(maxsize=200)
host = socket.gethostbyname(socket.gethostname())
global buffer
buffer = 999999

def vidRcv():
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
