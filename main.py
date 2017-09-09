'''
    Socket server to manage bank accounts of all players in game
    main thread listens to socket and connects clients
    makes a new thread for each client to send and receive
'''

import socket, sys, socketserver, threading
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8880 # Arbitrary non-privileged port
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
        parse = message.split(' ') #splits message into array of strings
        command = parse.pop(0)

        print("command received: " + message)

        if(command == 't'): #request transfer money t 1 2 200 = transfer player 1 sends player 2, $200
            parse = [int(i) for i in parse] #convert list of strings to int
            # get the to player num from message
            if(parse[1] == -1): #if player is trying to pay/withdraw money to bank
                if(parse[2] >= 0): #if paying the bank
                    self.updateAccount(parse[0], -parse[2]) #update from player account
                
                else:
                    self.askConfirm(0, message)

            else: #player to player transactions
                toPlayer = parse[1]
                self.askConfirm(toPlayer, message)

        elif(command == 'y'): #confirmed transfer money y 1 2 200 = transfer player 1 sends player 2, $200
            parse = [int(i) for i in parse] #convert list of strings to int
            self.updateAccount(parse[0], -parse[2]) #update from player account
            self.updateAccount(parse[1], parse[2]) #update to player account

        elif(command == 'b'): #confirmed bank withdrawal b 2 -1 -200 = player 2 withdraws $200
            parse = [int(i) for i in parse] #convert list of strings to int
            self.updateAccount(parse[0], -parse[2]) #update from player account

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

    def updateAccount(self, player, amount):
        print("amount: " + str(amount))
        
        bank[player] += amount

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