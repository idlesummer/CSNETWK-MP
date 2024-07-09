# Standard library imports
import importlib
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
        path_exists = Path(data_path).mkdir(parents=True, exist_ok=True)
        
        print('Server: Starting...')
        print(f"Server: {'Created' if path_exists else 'Used'} client storage at '{data_path}'")
        
        self.load_commands()       
        self.handle_sessions()
    
    def load_commands(self):
        for command_path in Path(self.commands_path).glob('*.py'):
            module_name = command_path.stem

            try:
                command_module = importlib.import_module(f'{Path(self.commands_path).name}.{module_name}')
                command_name = command_module.data['name']
                self.command_objs[command_name] = { 'data': command_module.data, 'validator': None }
                validation_path = Path(self.validations_path) / command_path.name
                
                if validation_path.exists() and validation_path.is_file():
                    validation_module = importlib.import_module(f'{Path(self.validations_path).name}.{module_name}')
                    validator = validation_module.validator
                    self.command_objs[command_name]['validator'] = validator
                    
                print(f"Server: Loaded command '{command_name}' from '{command_path}'")
                            
            except Exception as e:
                print(f"Server: Failed to load command from '{command_path}': {e}")
        
        print('Server: Loaded commands successfully.\n')
    
    def handle_sessions(self):
        while True:
            print('Server: Waiting for client connections..')
            client, addr = self.server.accept()
            session = Session(self.server, client, addr)
            thread = threading.Thread(target=self.client_connect, args=(session,))
            thread.start()
    
    def client_connect(self, session):
        print('Server: Accepted client connection.')
        session.client.send(b'Connection to the File Exchange Server is successful!')
        
        while True:
            try:
                message = session.client.recv(4096).decode()
            except ConnectionResetError:
                print('Server: Client has disconnected unexpectedly.')
                break
                
            if not message:
                print('Server: Client has been disconnected.')
                break
            
            interaction = Interaction(session, message)
            if interaction.is_command():
                self.client_interact(interaction)

    def client_interact(self, interaction):        
        command_name = interaction.command_name
        command_obj = self.command_objs.get(command_name)
        command_run = command_obj['data']['run']
        
        try:
            # Interaction validations
            if self.validate_interaction(interaction, command_obj):
                return
                        
            command_run(interaction, self)

        except Exception as e:
            print(e)
    
    def validate_interaction(self, interaction, command_obj):
        # Check if command exists
        if command_obj is None:
            interaction.client.send(b'Error: Command not found.')
            return True
        
        # Check for incorrect argument length        
        if len(interaction.options) != len(command_obj['data']['options']):
            interaction.client.send(b'Error: Command parameters do not match or is not allowed.')
            return True
        
        # Command-specific validations
        if command_obj['validator'] is not None and command_obj['validator'](interaction, command_obj, self):
            return True
        
        # Check for incorrect data type (to be implemented)
        return False
