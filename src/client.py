# Standard package imports
from socket import *

# Internal package imports
from lib import Session

client = socket(AF_INET, SOCK_STREAM)

session = Session(client)
response = session.connect(('localhost', 12345))

print(response.data)

while True:
    session.send({'cmd': 'dir'})
    response = session.receive()
    
    print(response.data)
    
    session.close()
    break
