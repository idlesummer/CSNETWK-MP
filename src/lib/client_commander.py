# Standard package imports
from base64 import b64encode
from pathlib import Path
from socket import *

# Internal package imports
from .import_file import import_file
from .interaction import Interaction
from .session import Session


class ClientCommander:
    
    def __init__(self, addr):
        self.addr = addr
        self.command_objs = {}
        
        self.handle_session()
        
        
    def handle_session(self):
        
        # Main loop
        while True:
            self.client = socket(AF_INET, SOCK_STREAM)
            self.session = Session(self.client)

            # Session loop            
            while True:
                # Get user interaction input
                prompt = input('Client> ')
                interaction = Interaction(prompt)
                
                # Check if interaction is command
                if not interaction.is_command():
                    print('> Client Invalid command.')
                    self.session.close()
                    return
                
                # Handle special commands
                
                if interaction.command == 'join':
                    
                    # Validations
                    # Check if arg length match
                    if len(interaction.args) != 2:
                        print('Error: Command parameters do not match or is not allowed.')
                        continue
                    
                    response = self.session.connect(self.addr)
                    
                    # Check if addr is correct
                    if response is None:
                        self.session.close()
                        print('Error: Connection to the Server has failed! Please check IP Address and Port Number.')
                        break
                    
                    print(response.data['msg'])
                    
                elif interaction.command == 'leave':
                    # send command to server
                    request = interaction.to_json()
                    self.session.send(request)
                    
                    # receive response
                    response = self.session.receive()
                    
                    # print response to user
                    print(response.data['msg'])
                    self.session.close()
                    break
                
                elif interaction.command == '?':
                    request = interaction.to_json()
                    self.session.send(request)
                    response = self.session.receive()
                    
                    commands_list = response.data['msg'].strip().split('\n')
                    commands_list.append('/join <server_ip_add> <port>')
                    commands_list.append('/store <filename>')
                    commands_list.sort()
                    
                    if '/store <filename> <file-data>' in commands_list:
                        commands_list.remove('/store <filename> <file-data>')

                    print(f'\nCommands List\n{'\n'.join(commands_list)}\n')
                    
                elif interaction.command == 'store':
                    filename = interaction.args[0]
                    
                    if not Path(filename).exists():
                        print('Error: File not found.')
                        continue
                    
                    file_bytes = b''
                    with open(filename, 'rb') as file:
                        file_bytes = file.read()
                    
                    # send command to server
                    encoded_file_data = b64encode(file_bytes).decode('utf-8')
                    request = {'cmd': 'store', 'args': [filename, encoded_file_data]}
                    self.session.send(request)
                    
                    # receive response
                    response = self.session.receive()
                    
                    # print response to user
                    print(response.data['msg'])
                          
                else:
                    # send command to server
                    request = interaction.to_json()
                    self.session.send(request)
                    
                    # receive response
                    response = self.session.receive()
                    
                    # print response to user
                    print(response.data['msg'])
