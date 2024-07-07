import asyncio
import importlib
import os
from pathlib import Path
from pyee import AsyncIOEventEmitter


class Commander:
    
    def __init__(self, server, commandsPath):
        self.server = server
        self.commandsPath = commandsPath
        self.ee = AsyncIOEventEmitter() 
        self.commands = {}
        
        self.register_events()
        self.build_commands()
        asyncio.create_task(self.handle_commands())
    
    def register_events(self):
        self.ee.on('client-connect', self.client_connect)
    
    def build_commands(self):
        for file in os.listdir(self.commandsPath):
            module_name = file[:-3]
            
            try:
                module = importlib.import_module(f'{Path(self.commandsPath).name}.{module_name}')
                name = module.data.name
                self.commands[name] = module.data
            
            except ImportError as e:
                print(f"Error importing module '{module_name}': {e}")
    
    async def handle_commands(self):
        while True:
            client, addr = await self.server.accept()
            self.ee.emit('client-connect', self.server, client, addr)
    
    async def client_connect(self, server, client, addr):
        client.send('Connection to the File Exchange Server is successful!'.encode())
        
        while True:
            message = client.recv(4096).decode().split()
            command_name = message[0][1:]
            command = self.commands[command_name]
            command.run(*message[1:])
            
            
    