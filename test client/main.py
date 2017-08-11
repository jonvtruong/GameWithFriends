import socket, sys

HOST = socket.gethostname()                           
PORT = 8888
player = 0
account = 0
playerNames = []
def gameProtocol(message):
    '''
    messages will be in the format: a 200 = total account value 200

    '''
    parse = message.split(' ')
    command = parse.pop(0)

    if(command == 'n'): #if creating new player, update player number and account starting balance
        player, account = parse
        print("Player number: " + player + " account balance: " + account)
        
    elif(command == 'a'):
        print('parse: ' + str(parse))
        account = int(*parse)
        print('account updated: ' + str(account))
    
if(__name__ == '__main__'):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # connection to hostname on the port.
    s.connect((HOST, PORT))                               
    decode = s.recv(64).decode()
    print("connected " + decode)
    gameProtocol(decode)
    message = input("Input: ")

    while True:
        s.sendall(message.encode())
        data = s.recv(64)
        
        if(len(data) > 0):
            decode = data.decode()
            print("Client received: " + decode)

            if(message == 'quit'):
                break
            else:
                gameProtocol(decode)

            message = input("Input: ")                                     

    s.close()
    sys.exit()