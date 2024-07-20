# Standard package imports
from pathlib import Path
from socket import *

# Internal package imports
from lib import ClientCommander

# Client setup
ip, port = 'localhost', 12345

client = ClientCommander(addr=(ip, port))
