# Standard library imports
import importlib
import os
from pathlib import Path
import threading

# Internal package imports
from .interaction import Interaction
from .session import Session


class Commander:
    
    def __init__(self, server, commands_path, data_path, validations_path):
        self.server = server
        self.commands_path = commands_path
        self.data_path = data_path
        self.validations_path = validations_path
        self.command_objs = { }
        
        self.load_commands()       
        self.handle_sessions()
    
    def load_commands(self):
        for filename in os.listdir(self.commands_path):
            if not filename.endswith('.py'):
                continue
            
            module_name = Path(filename).stem
            try:
                command_module = importlib.import_module(f'{Path(self.commands_path).name}.{module_name}')
                command_name = command_module.data['name']
                self.command_objs[command_name] = { 
                    'data': command_module.data, 
                    'validation': None, 
                }
                validation_exists = os.path.exists(os.path.join(self.validations_path, filename))
                                
                if validation_exists:
                    validation_module = importlib.import_module(f'{Path(self.validations_path).name}.{module_name}')
                    validation = validation_module.validate
                    self.command_objs[command_name]['validation'] = validation
                            
            except ImportError as e:
                print(f"Server: Error importing command module '{module_name}': {e}")
    
    def handle_sessions(self):
        while True:
            print('Server: Waiting for client connections..')
            client, addr = self.server.accept()
            session = Session(self.server, client, addr)
            thread = threading.Thread(target=self.client_connect, args=(session,))
            thread.start()
    
    def client_connect(self, session):
        print('Server: Accepted client connection.')
        session.client.send('Connection to the File Exchange Server is successful!'.encode())
        
        while True:
            message = session.client.recv(4096).decode()
            if not message:
                print('Server: Client has been disconnected.')
                break
            
            interaction = Interaction(session, message)
            if interaction.is_command():
                self.client_interact(interaction)

    def client_interact(self, interaction):        
        command_name = interaction.command_name
        command_obj = self.command_objs.get(command_name)
        
        try:
            # Interaction validations
            if self.validate_interaction(interaction, command_obj):
                return
                        
            command_obj['data']['run'](interaction, self)

        except Exception as e:
            print(e)
    
    def validate_interaction(self, interaction, command_obj):
        # Check if command exists
        if command_obj is None:
            interaction.client.send('Error: Command not found.'.encode())
            return True
        
        # Check for incorrect argument length        
        if len(interaction.options) != len(command_obj['data']['options']):
            interaction.client.send('Error: Command parameters do not match or is not allowed.'.encode())
            return True
        
        # Command-specific validations
        if command_obj['validation'] is not None and command_obj['validation'](interaction, command_obj, self):
            return True
        
        # Check for incorrect data type (to be implemented)
        return False
