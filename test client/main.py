import socket, sys

HOST = socket.gethostname()                           
PORT = 8888
PLAYER = 0
ACCOUNT = 0

def parseMessage(message):
    '''
    messages will be in the format: 1 200 = player 1, total account value

    '''
    parse = message.split(' ')

    if(len(parse) == 2):
        return parse
    else:
        return None

if(__name__ == '__main__'):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # get local machine name


    # connection to hostname on the port.
    s.connect((HOST, PORT))                               
    tm = s.recv(1024).decode()
    print("connected " + tm)
    
    PLAYER, ACCOUNT = parseMessage(tm)
    PLAYER = int(PLAYER)
    ACCOUNT = int(ACCOUNT)

    print("Player number, account balance: " + tm)
    message = input("Input: ")

    while True:
        s.sendall(message.encode())
        tm = s.recv(1024)
        print("Client received: " + str(tm.decode()))

        if(message == 'quit'):
            break
        else:
            parseMessage(message)

        message = input("Input: ")                                     

    s.close()
    sys.exit()