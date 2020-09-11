import socket
import pickle #turns objects into bytes to be sent over the network

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1" #has to be the same as the one used in server file
        self.port = 50000
        self.addr = (self.server, self.port)
        self.p = self.connect() #willhelp later in sending an ID to the client so they know if they are player 1, player 2, etc...
       
    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr) #trying to connect 
            return self.client.recv(2048).decode() #loads byte data
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data)) #sending string data 
            return pickle.loads(self.client.recv(2048*2)) #receving pickle object to load into bytes
        except socket.error as e:
            print(e)


