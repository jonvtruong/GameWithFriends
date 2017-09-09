'''
    Socket server to manage bank accounts of all players in game
    main thread listens to socket and connects clients
    makes a new thread for each client to send and receive
'''

import socket, sys, socketserver, threading
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
START_ACCOUNT = 1500
bank = []
playerConn = []
playerNames = []
BUFFER_SIZE = 128

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ManageClient(socketserver.BaseRequestHandler):
    '''
    Request handler class for server
    Instantiated for each client connection
    '''

    def setup(self):
        print("connected to " + str(self.client_address))
        self.newPlayer()

    def handle(self):
        while True:
        #now keep talking with the client
        #wait to accept a connection - blocking call
            try: 
                data = self.request.recv(BUFFER_SIZE)

                if(len(data) > 0):
                    decode = data.decode()
                    if (decode == 'quit'):
                        print("quit")
                        break

                    else:
                        self.gameProtocol(decode)

                else:
                    break

            except ConnectionResetError:
                print("connection broken") 
                break

    def finish(self):
        print("closing connection with " + str(self.client_address))
        playerConn[playerConn.index(self.request)] = False    
        self.request.close()

        if(not any(playerConn)): #if no more players connected then close server
            print("No more players, closing server")
            self.server.shutdown()
            
    def gameProtocol(self, message):
        '''
        messages will be in the format: t 1 2 200 = transfer player 1 sends player 2, $200
        returns a tuple of strings
        '''
        parse = message.split(' ')
        command = parse.pop(0)

        print("command received: " + message)

        if(command == 't'): #request transfer money t 1 2 200 = transfer player 1 sends player 2, $200
            # get the to player num from message
            toPlayer = int(parse[1])
            self.askConfirm(toPlayer, message)

        elif(command == 'y'): #confirmed transfer money y 1 2 200 = transfer player 1 sends player 2, $200
            parse = [int(i) for i in parse] #convert list of strings to int
            self.updateAccount(*parse) #unpacks list into 3 arguments: from, to, amount

        elif(command == 'n'): #new player created (message = n Name)
            playerNames.append(parse[0])
            print("name received: " + parse[0])
            self.sendNames()

    def sendNames(self): #sends list of names to all players
        nameList = ' '.join(name for name in playerNames)
       # nameList = 'p '.join(nameList)
        print("sending list: " + nameList)  
        message = 'p ' + nameList

        for conn in playerConn: #send the latest name list to all players
            conn.sendall(message.encode())

    def updateAccount(self, fromPlayer, toPlayer, amount):
        print("amount: " + str(amount))
        
        bank[fromPlayer] -= amount
        bank[toPlayer] += amount
        self.sendAccount(fromPlayer)
        self.sendAccount(toPlayer)
    
    def sendAccount(self, player):
        message = 'a ' + str(bank[player])
        print("sending player message: " + message)
        playerConn[player].sendall(message.encode())

    def askConfirm(self, to, m):
        print("sending ToPlayer message: " + m)
        playerConn[to].sendall(m.encode())

    def newPlayer(self):
        playerConn.append(self.request)
        playerNum = playerConn.index(self.request)
        bank.append(START_ACCOUNT)

        #sends the player their player number and starting balance

        message = 'n ' + str(playerNum) + " " + str(bank[playerNum])
        self.request.sendall(message.encode())
        print("new player added, sending: " + message)

if(__name__ == '__main__'):
    server = ThreadedTCPServer((HOST, PORT), ManageClient)
    print('Socket listening')
    
    server.serve_forever()