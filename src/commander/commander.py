from pyee import AsyncIOEventEmitter


class Commander:
    
    def __init__(self, server, commandsPath):
        self.server = server
        self.commandsPath = commandsPath
        self.ee = AsyncIOEventEmitter() 
                        
        self.build_commands()
        self.handle_commands()
    
    def build_commands(self):
        pass
    
    def handle_commands(self):
        while True:
            client, addr = self.server.accept()
            self.ee.emit('client-connect', client, addr)
