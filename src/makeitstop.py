import cv2


capture =  cv2.VideoCapture("http://192.168.1.32:9999/stream.mjpg")

while(True):
    _, frame = capture.read()
    cv2.imshow('stream', frame)
    if cv2.waitKey(1)==ord("q"):
        break
    
capture.release()
cv2.destroyAllWindows()