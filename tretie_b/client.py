import socket

import socket
CLIENT_IP = "147.175.161.195" # client host ip A.B.C.D
CLIENT_PORT = 50601 # client port for recieving communication
SERVER_IP = "147.175.162.153"
SERVER_PORT = 50601

class Client:

    def __init__(self, ip, port, server_ip, server_port) ->None:
        self.sock = socket.socket(socket.AF_INET,
        socket.SOCK_DGRAM) # UDP socket creation
        self.server_ip = server_ip
        self.server_port = server_port

    def receive(self):
        data = None
        data, self.server = self.sock.recvfrom(1024) # buffer size is 1024 bytes
        return data #1

    def send_message(self, message):
        self.sock.sendto(bytes(message,encoding="utf8"),(self.server_ip,self.server_port))

    def quit(self):
        self.sock.close() # correctly closing socket
        print("Client closed..")


if __name__ == "__main__":
    client = Client(CLIENT_IP, CLIENT_PORT, SERVER_IP,SERVER_PORT)
    data = "empty"
    print("Input your message: ") #1
    client.send_message(input()) # 1
    data = client.receive() # 1
    if data != None: # 1
        print(data) # 1
    else: # 1
        print("Message has not been received")  # 1
        client.quit()