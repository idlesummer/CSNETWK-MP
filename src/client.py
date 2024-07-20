# Standard package imports
from socket import *

# Internal package imports
from lib import Session

client = socket(AF_INET, SOCK_STREAM)

session = Session(client)
response = session.connect(('localhost', 12345))

print(response.data)

while True:
    
    # get user input
    prompt = input('Client> ')
    
    # process command
    if not prompt.startswith('/'):
        print('Closing session')
        session.close()
        break
        
    tokens = prompt.split()
    symbol = tokens[0][0]
    command = tokens[0][1:]
    args = tokens[1:]
    
    print(tokens)
    print(symbol)
    print(command)
    print(args)
        
    # send command to server
    session.send({'cmd': command, 'args': args})
    
    # receive response
    response = session.receive()
    
    # print response to user
    print(response.data)
