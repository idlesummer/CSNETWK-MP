# Standard library imports
import importlib
from pathlib import Path
import threading

# Internal package imports
from .interaction import Interaction
from .session import Session


class Commander:
    
    def __init__(self, server, commands_path, data_path):
        self.server = server
        self.commands_path = commands_path
        self.data_path = data_path
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
                command_obj = command_module.data
                command_name = command_obj['name']
                
                # Populate optional properties with default values
                command_obj['options'] = command_obj.get('options') or { }
                command_obj['validator'] = command_obj.get('validator') or None

                # Add command object to collection
                self.command_objs[command_name] = command_obj                
                print(f"Server: Loaded command '{command_name}' from '{command_path}'")
                            
            except Exception as e:
                print(f"Server: Failed to load command from '{command_path}': {e}")
    
    def handle_sessions(self):
        while True:
            print('Server: Waiting for client connections..')
            client, addr = self.server.accept()
            session = Session(self.server, client, addr)
            thread = threading.Thread(target=self.client_connect, args=(session,))
            thread.start()
    
    def client_connect(self, session):
        print('Server: Accepted client connection.')
        session.client.send(b'DISPLAY Connection to the File Exchange Server is successful!')
        
        while True:
            try:
                message = session.client.recv(4096).decode()
            except ConnectionResetError:
                print('Server: Client has disconnected unexpectedly.')
                break
                
            if not message:
                session.client.close()
                print('Server: Client has been disconnected.')
                break
            
            interaction = Interaction(session, message)
            if interaction.is_command():
                self.client_interact(interaction)
            else:
                session.client.send(b'DISPLAY u dint provide a command!')

    def client_interact(self, interaction):        
        session = interaction.session
        command_name = interaction.command_name
        command_obj = self.command_objs.get(command_name)
        
        if command_obj is None:
            session.client.send(b'DISPLAY Error: Command not found.')
            return       
        
        command_run = command_obj['run']

        try:
            # Validate interaction
            if self.validate_interaction(interaction, command_obj):
                return

            command_run(interaction, self)

        except Exception as e:
            print(e)
    
    def validate_interaction(self, interaction, command_obj):
        # Check if command exists
        if command_obj is None:
            interaction.client.send(b'DISPLAY Error: Command not found.')
            return True
        
        # Check for incorrect argument length        
        if command_obj['options'] is not None and len(interaction.options) != len(command_obj['options']):
            interaction.client.send(b'Error: Command parameters do not match or is not allowed.')
            return True

        # Command-specific validations
        if command_obj['validator'] is not None and command_obj['validator'](interaction, command_obj, self):
            return True
        
        # Check for incorrect data type (to be implemented)
        return False
