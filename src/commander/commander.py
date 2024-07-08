import importlib
import os
from pathlib import Path
import threading

from .interaction import Interaction
from .session import Session


class Commander:
    
    def __init__(self, server, commandsPath, dataPath, validationsPath):
        self.server = server
        self.commandsPath = commandsPath
        self.dataPath = dataPath
        self.validationsPath = validationsPath
        self.command_objs = {}
        
        self.load_commands()       
        self.handle_commands()
    
    def load_commands(self):
        for filename in os.listdir(self.commandsPath):
            if not filename.endswith('.py'):
                continue
            
            module_name = Path(filename).stem
            try:
                command_module = importlib.import_module(f'{Path(self.commandsPath).name}.{module_name}')
                command_name = command_module.data['name']
                self.command_objs[command_name] = { 'data': command_module.data }
                self.command_objs[command_name]['validation'] = None
                validation_exists = os.path.exists(os.path.join(self.validationsPath, filename))
                                
                if validation_exists:
                    validation_module = importlib.import_module(f'{Path(self.validationsPath).name}.{module_name}')
                    validation = validation_module.validate
                    self.command_objs[command_name]['validation'] = validation
                            
            except ImportError as e:
                print(f"Server: Error importing command module '{module_name}': {e}")
    
    def handle_commands(self):
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
        command_obj = self.command_objs[command_name]  
        
        try: 
            if not self.validate_interaction(interaction, command_obj):
                return
            
            if command_obj['validation'] is not None and not command_obj['validation'](interaction, command_obj, self):
                return
            
            command_obj['data']['run'](interaction, self)

        except Exception as e:
            print(e)
    
    def validate_interaction(self, interaction, command_obj):
        # Check for incorrect argument length
        if len(interaction.options) != len(command_obj['data']['options']):
            return False
        
        # Check for incorrect data type
        return True
