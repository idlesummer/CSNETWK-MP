# Standard package imports
import json
from socket import *

from lib import Message

client = socket(AF_INET, SOCK_STREAM)

client.connect(('localhost', 12345))

# Receive welcome message
message_length_byte = client.recv(4)
message_length = int.from_bytes(message_length_byte, byteorder='big')
message = b''

while len(message) < message_length:
    chunk = client.recv(4096)

    if not chunk:
        raise ConnectionError("Client disconnected before sending full message.")

    message += chunk

# Parse the message
message = message.decode()

print(message)


# Sending message

message = json.dumps({'cmd': '?'})
message_bytestr = json.dumps(message).encode('utf-8')
message_length = len(message_bytestr).to_bytes(4, byteorder='big')

# Send the message length
client.sendall(message_length)

# Send the actual message data
client.sendall(message_bytestr)

# Receiving message

message_length_byte = client.recv(4)
message_length = int.from_bytes(message_length_byte, byteorder='big')
message = b''

while len(message) < message_length:
    chunk = client.recv(4096)

    if not chunk:
        raise ConnectionError("Client disconnected before sending full message.")

    message += chunk

# Parse the message
message = message.decode()

print(message)

