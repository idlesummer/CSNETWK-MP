import json
from pathlib import Path
from src.shared import Communicator


class Session:
    def __init__(self, server, client, data_path):
        self.server = server
        self.client = client
        self.data_path = data_path
        self.communicator = Communicator(client)
        self.handle = None
        self.storage_path = None
        
    def register(self, handle):
        if self.is_registered():
            return False
        
        # Validate if filename handle        
        storage_path = Path(self.data_path) / handle
        storage_path.mkdir(parents=True, exist_ok=True)
        self.storage_path = str(storage_path)
        
        return storage_path
    
    def is_registered(self):
        return self.handle is not None
    
    def send(self, type, body):    
        try:
            message = json.dumps({'type': type, 'body': body})
            status = self.communicator.send(message)
            
            if status is None:
                print('Error: Error sending message.')
                return False
            
        except json.JSONEncodeError as e:
            print('Server: Error sending message: {e}')
        
    def receive(self):
        try:
            message = self.communicator.receive()
            return json.loads(message)
        
        except (ConnectionError, OSError) as e:
            print(f'Server: Error receiving message: {e}')
            return None
