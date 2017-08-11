'''
    Socket server to manage bank accounts of all players in game
    main thread listens to socket and connects clients
    makes a new thread for each client to send and receive
'''

import socket, sys, socketserver, threading
 
HOST = '192.168.1.108'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
START_ACCOUNT = 1500
bank = [0,10000]
playerConn = []
playerNames = []

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ManageClient(socketserver.BaseRequestHandler):
    '''
    Request handler class for server
    Instantiated for each client connection
    '''
    # def __init__(self, conn):
    #     super.__init__(self)
    #     self.conn = conn

    def setup(self):
        print("connected to " + str(self.client_address))
        newPlayer(self.request)

    def handle(self):
        while True:
        #now keep talking with the client
        #wait to accept a connection - blocking call
        try: 
            data = conn.recv(64)

            if(len(data) > 0):
                decode = data.decode()
                if (decode == 'quit'):
                    print("quit")
                    break

                else:
                    gameProtocol(decode)

            else:
                break

        except ConnectionResetError:
            print("connection broken")
            break
            
        s.close()
        sys.exit()
            
    def gameProtocol(message):
        '''
        messages will be in the format: t 1 2 200 = transfer player 1 sends player 2, $200
        returns a tuple of strings
        '''
        parse = message.split(' ')
        command = parse.pop(0)

        if(command == 't'): #transfer money t 1 2 200 = transfer player 1 sends player 2, $200
            parse = [int(i) for i in parse] #convert list of strings to int
            updateAccount(*parse) #unpacks list into 3 arguments: from, to, amount

        elif(command == 'n'): #new player created (message = n Name)
            playerNames.append(parse[0])
            print("name: " + parse[0])

    def updateAccount(fromPlayer, toPlayer, amount):
        bank[fromPlayer] -= amount
        bank[toPlayer] += amount
        sendFrom(fromPlayer)
        #sendTo(fromPlayer, toPlayer, amount) 

    def sendFrom(player):
        message = 'a ' + str(bank[player])
        print("sending message: " + message)
        playerConn[player].sendall(message.encode())

    def sendTo(fromPlayer, toPlayer, amount):
        message = 't ' + str(fromPlayer) + ' ' + str(toPlayer) + ' ' + str(amount)
        print("sending message: " + message)
        playerConn[toPlayer].sendall(message.encode())

    def newPlayer(conn):
        playerConn.append(conn)
        playerNum = playerConn.index(conn) #playerNum is int
        bank[playerNum]=START_ACCOUNT

        #sends the player their player number and starting balance

        message = 'n ' + str(playerNum) + " " + str(bank[playerNum])
        conn.sendall(message.encode())
        print("new player added: " + message)

if(__name__ == '__main__'):
    server = ThreadedTCPServer((HOST, PORT), ManageClient)
    print('Socket listening')
    
    server.serve_forever()