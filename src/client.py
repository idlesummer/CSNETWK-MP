from socket import *

client = socket(AF_INET, SOCK_STREAM)

client.connect(('localhost', 12345))

print(client.recv(4096).decode())

while True:
    message = input('Client: ')
    
    if message.lower() == 'exit':
        break
    
    client.send(message.encode())
    print(f'Server: {client.recv(4096).decode()}')
