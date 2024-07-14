# Standard library imports
from pathlib import Path
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
commands_path = Path.cwd() / 'src/commands'
data_path = Path.cwd() / 'public/data'

Commander(
    server=server,
    commands_path=commands_path,
    data_path=data_path,
)
