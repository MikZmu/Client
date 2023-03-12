import socket

host = socket.gethostbyname(socket.gethostname())
port = 9999
listener  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.connect((host, port))
def phobos_listen():
        done = False

        while not done:
                message = input("Message: ")
                listener.send(message.encode('utf-8'))
                incoming = listener.recv(4096).decode('utf-8')
                if message == " ":
                        listener.close()
                        done = True
                else:
                        print(incoming)
                #communication_socket.close())

phobos_listen()