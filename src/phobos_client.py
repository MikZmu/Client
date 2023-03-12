import socket

host = socket.gethostbyname(socket.gethostname())
port = 2137
def phobos_listen():
        listener  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.connect((host, port))
        listener.send("Hello world !".encode('utf-8'))
        print(listener.recv(4096))