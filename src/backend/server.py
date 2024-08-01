# Standard package imports
from pathlib import Path
from socket import *

# Internal package imports
from lib import Server

# Server setup
ip, port = '127.0.0.1', 12345
server = socket(AF_INET, SOCK_STREAM)
server.bind((ip, port))

# Server startup
server.listen()

# Command handler configurations
commands_path = Path.cwd() / 'commands'
storage_path = Path.cwd().parent.parent / 'public/data'

Server(
    server=server,
    commands_path=commands_path,
    storage_path=storage_path,
)
