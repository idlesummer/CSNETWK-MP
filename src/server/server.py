# Standard package imports
from pathlib import Path
from socket import *

# Internal package imports
from commander import Commander

# Server setup
ip, port = 'localhost', 12345
server = socket(AF_INET, SOCK_STREAM)
server.bind((ip, port))

# Server startup
server.listen()

# Command handler configurations
commands_path = Path.cwd() / 'src/server/commands'
data_path = Path.cwd() / 'public/data'

Commander(
    server=server,
    commands_path=commands_path,
    data_path=data_path,
)
