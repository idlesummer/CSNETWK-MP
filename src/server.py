# Standard library imports
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
    commands_path=os.path.join(os.getcwd(), 'src/commands'),
    data_path=os.path.join(os.getcwd(), 'data'),
    validations_path=os.path.join(os.getcwd(), 'src/validations'),
)
