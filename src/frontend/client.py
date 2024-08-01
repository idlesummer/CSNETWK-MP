# Standard imports
from pathlib import Path
from socket import *

# Internal imports
from lib import Client

# Client configurations
commands_path = Path.cwd() / 'commands'

# Client main
client = Client(
    commands_path=commands_path,
)
