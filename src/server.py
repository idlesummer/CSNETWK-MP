# Builtin package imports
import os
from socket import *

# Internal package imports
from commander import Commander

# Server setup
addr, port = 'localhost', 12345
server = socket(AF_INET, SOCK_STREAM)
server.bind((addr, port))

# Server startup
server.listen()

# Command handler configurations
Commander(
    server=server,
    commandsPath=os.path.join(os.getcwd(), 'commands')
)
