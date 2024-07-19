# Standard package imports
from pathlib import Path
from socket import *

# Internal package imports
from lib import ServerCommander

# Server setup
ip, port = 'localhost', 12345
server = socket(AF_INET, SOCK_STREAM)
server.bind((ip, port))

# Server startup
server.listen()

# Command handler configurations
commands_path = Path.cwd() / 'src/commands/server'
data_path = Path.cwd() / 'public/data'

print('Main', commands_path)


ServerCommander(
    server=server,
    commands_path=commands_path,
    data_path=data_path,
)
