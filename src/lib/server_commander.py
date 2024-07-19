# Standard package imports
import importlib
import os
from pathlib import Path
import threading

# Internal package imports
from .import_file import import_file
from .session import Session


class ServerCommander:
    
    def __init__(self, server, commands_path, data_path):
        self.server = server
        self.commands_path = commands_path
        self.data_path = data_path
        self.command_objs = { }
        
        print('Server: Starting...')
        print(f"Server: Used client storage at '{data_path}'")
        
        self.load_commands()
        self.handle_sessions()
        
        
    def load_commands(self):        
        for command_path in Path(self.commands_path).glob('*.py'):
            try: command_module = import_file(command_path.stem, command_path)
            
            except (ImportError, OSError) as e:
                print(f"Server: Failed to load command from '{command_path}': {e}")
                continue
            
            command_obj = command_module.data
            command_name = command_obj.get('name', None)                                

            # Populate optional properties with default values
            command_obj['options'] = command_obj.get('options', {})
            command_obj['validator'] = command_obj.get('validator', None)

            # Add command object to collection
            self.command_objs[command_name] = command_obj
            print(f"Server: Loaded command '{command_name}' from '{command_path}'")
            
            
    def handle_sessions(self): 
        while True:
            print('Server: Waiting for client connections...')
            client, _ = self.server.accept()
            session = Session(client)
            session.data['server'] = self.server
            session.data['data_path'] = self.data_path
            
            thread = threading.Thread(target=self.on_connect, args=(session,))
            thread.start()
            
            
    def on_connect(self, session):
        # Configure session
        session.set_timeout(60_000)
        
        # Log successful connection
        print('Server: Accepted client connection.')
        session.send({ 'msg': 'Connection to the File Exchange Server is successful!' })
              
        while True:
            # Wait for client request
            request = session.receive()
            
            # Handle time-out disconnection
            if request.timed_out: 
                session.close()
                print('Server: Client has timed out.')
                break
            
            # Handle unexpected disconnection
            if request.disconnected:
                session.close()
                print('Server: Client has been disconnected')
                break

            self.on_request(session, request) 
                  
                                
    def on_request(self, session, request):
        command_name = request.body['cmd']
        command_obj = self.command_objs.get(command_name)
    
        try:
            # Validate interaction
            if self.validate_request(session, command_obj):
                return
            
            command_run = command_obj['run']
            command_run(session, request, self)

        except Exception as e:
            print(e)
        
    def validate_request(self, session, request, command_obj):
        
         # Check if command exists
        if command_obj is None:
            session.send({'status': 'ERROR', 'msg': 'Error: Command not found.'})
            return True
        
        # Check for incorrect argument length        
        if command_obj['options'] is not None and len(request.options) != len(command_obj['options']):
            session.send({'status': 'ERROR', 'msg': 'Error: Command parameters do not match or is not allowed.'})
            return True

        # Command-specific validations
        if command_obj['validator'] is not None and command_obj['validator'](session, request, command_obj, self):
            validator_message = command_obj.get('validator_message') or 'COMMAND-ERROR'
            session.send({'status': 'ERROR', 'msg': validator_message})
            return True
        
        # Check for incorrect data action (to be implemented)
        return False

