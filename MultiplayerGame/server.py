#needed to handle connections to server
import socket
from _thread import *
import sys
from player import player
import pickle
from game import Game


#server = "192.168.1.79" #ipconfig
server = "127.0.0.1"
port =  50000 #an unused port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #two types of connections. we are connecting to IPv4 address so that is reason for 1st variable #second variable helps read in server string value

#trying and excepting our port server bind to see if the port is open for use
try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen()

print("Waiting for a connection, Server Started.")

connected = set()
games = {}
idCount = 0

def threaded_client(conn , p, gameId): #threaded clients will run as a background process, they dont have to finish executing for main process to run
     global idCount
     conn.send(str.encode(str(p))) #sending the client what player they are (0 or 1)

     reply = ""
     
     while True: #sending either get, reset, move (R P S). sending get means we are getting game from server and giving to client. reset means reset the game after both players played (sent from client to server). move is sent from client to server, updated in server, and then the game is sent back to client
         try: 
             data = conn.recv(4096).decode()
             if gameId in games: 
                 game = games[gameId] #everytime we run the while loop, we will check if the game exists. this is to help delete games when or if a client disconnects

                 if not data:
                     break                      #this while loop is the heart of the server, sending and receiving the game to update the clients on both ends
                 else:
                     if data == "reset":
                         game.resetWent()
                     elif data != "get":
                         game.play(p, data)
                
                     reply = game
                     conn.sendall(pickle.dumps(reply)) #package the game into pickle object and send it to client to make moves and draw to screen etc. 
                     
             else: #this is in the case that the game no longer exists
                break
         except:
            break
        
     print("Lost connection.")

     try:
         del games[gameId] #deleting games, if both players disconnect the game at the same time, then one player will delete the game before the other. this might cause an attempt to delete nonexistent game for the second player trying to delete it. so we try it first
         
         print("Closing game: ", gameId)
     except:
         pass
     idCount -= 1
     conn.close()



while True: #this process will run at the front end to look for another possible connection

    conn, addr = s.accept() #accept() will accept a connection and store its object and IP in these variables
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2 #for every two clients, 1 game is created
    if idCount % 2 == 1: #creates a game for the odd numbered client who does not have a game (ex: if there are 3 players, 2 are in game and the third is waiting for a 4th to start a new game)
        games[gameId] = Game(gameId) #creating a game object as a gameId is created for two clients
        print("Creating a new game...") #server notification for new game being made
    else:
        games[gameId].ready = True #a second player has connected, which means the game started by the first odd numbered client is now ready to play. now the game is ready
        p = 1 #player = 1




    start_new_thread(threaded_client, (conn, p, gameId))


