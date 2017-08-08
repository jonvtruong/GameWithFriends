'''
    Socket server to manage bank accounts of all players in game
'''

import socket, sys
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
bank = [0,10000]
playerConn = []

def parseMessage(message):
    '''
    messages will be in the format: 1 2 200 = player 1 sends player 2, $200
    returns a tuple of strings
    '''
    parse = message.split(' ')
    
    if(len(parse) == 3):
        return parse
    else:
        return None

def updateAccount(fromPlayer, toPlayer, amount):
    bank[fromPlayer] -= amount
    bank[toPlayer] += amount

if(__name__ == '__main__'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
        
    print('Socket bind complete')
    
    #Start listening on socket
    s.listen(10)
    print('Socket now listening')
    
    #makes a connection and adds a new player
    conn, addr = s.accept()
    playerConn.append(conn)
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    playerNum = playerConn.index(conn) #playerNum is int

    bank[playerNum]=1500

    #sends the player their player number and starting balance
    message = str(playerNum) + " " + str(bank[playerNum])
    conn.sendall(message.encode())

    while True:
        #now keep talking with the client
        #wait to accept a connection - blocking call
        try: 
            data = conn.recv(1024)
        
            print("data length: " + str(len(data)))

            if(len(data) > 0):
                decode = data.decode()
                if (decode == 'quit'):
                    print("quit")
                    break

                else:
                    fr, to, am = parseMessage(decode)
                    updateAccount(int(fr), int(to), int(am))
                    message = str(bank[0])
                    print("sending: " + message)
                    conn.sendall(message.encode())
        except ConnectionResetError:
            print("connection broken")
            break
            
    s.close()
    sys.exit()