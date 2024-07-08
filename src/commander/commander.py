import asyncio
import importlib
import os
from pathlib import Path
import threading


class Commander:
    
    def __init__(self, server, commandsPath):
        self.server = server
        self.commandsPath = commandsPath
        self.commands = {}
        
        self.build_commands()       
        self.handle_commands()
    
    def build_commands(self):
        for filename in os.listdir(self.commandsPath):
            if not filename.endswith('.py'):
                continue
            
            module_name = Path(filename).stem
            try:
                module = importlib.import_module(f'{Path(self.commandsPath).name}.{module_name}')
                name = module.data['name']
                self.commands[name] = module.data
            
            except ImportError as e:
                print(f"Error importing command module '{module_name}': {e}")
    
    def handle_commands(self):
        while True:
            print('Server: Waiting for client connections..')
            client, addr = self.server.accept()
            thread = threading.Thread(target=self.client_connect, args=(self.server, client, addr))
            thread.start()
    
    def client_connect(self, server, client, addr):
        print('Server: Accepted client connection.')
        client.send('Connection to the File Exchange Server is successful!'.encode())
        
        while True:
            message = client.recv(4096).decode().split()
            self.client_interact(self.server, client, addr, message)
            
    def client_interact(self, server, client, addr, message):
        command_name = message[0][1:]
        command = self.commands[command_name]
        
        try: 
            command.run(*message[1:])
        except Error as e:
            print(e)
                