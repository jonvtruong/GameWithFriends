'''
    Socket server to manage bank accounts of all players in game
    main thread listens to socket and connects clients
    makes a new thread for each client to send and receive
'''

import socketserver 
import sys
import socket
import threading

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

playerConn = []
bank = []

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ConnectClient(socketserver.BaseRequestHandler):
    '''
    Request handler class for server
    Instantiated for each client connection
    '''
    # def __init__(self, conn):
    #     super.__init__(self)
    #     self.conn = conn

    def parseMessage(self, message):
        '''
        messages will be in the format: 1 2 200 = player 1 sends player 2, $200
        returns a tuple of strings
        '''
        parse = message.split(' ')
        
        if(len(parse) == 3):
            return parse
        else:
            return None

    def updateAccount(self, fromPlayer, toPlayer, amount):
        print("update")
        #bank[fromPlayer] -= amount
        #bank[toPlayer] += amount

    def setup(self):
        print("connected to " + str(self.client_address))
        playerConn.append(self.request)    
        playerNum = playerConn.index(self.request) #playerNum is int

        bank.append(1500)

        #sends the player their player number and starting balance
        message = str(playerNum) + " " + str(bank[playerNum])
        self.request.sendall(message.encode())

    def handle(self):
        while True:
            #now keep talking with the client
            #wait to accept a connection - blocking call
            try: 
                data = self.request.recv(1024)
            
                print("data length: " + str(len(data)))

                if(len(data) > 0):
                    decode = data.decode()
                    if (decode == 'quit'):
                        print("quit")
                        break

                    else:
                        fr, to, am = self.parseMessage(decode)
                        self.updateAccount(int(fr), int(to), int(am))
                        message = str(bank[0])
                        print("sending: " + message)
                        self.request.sendall(message.encode())

            except ConnectionResetError:
                print("connection broken")
                break
                
        self.request.close()

if(__name__ == '__main__'):
    #create server, bind and listen to socket
    server = ThreadedTCPServer((HOST, PORT), ConnectClient)
    print('Socket listening')
    
    server.serve_forever()