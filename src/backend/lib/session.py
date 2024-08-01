from .message import Message


class Session:
    
    def __init__(self, client):
        self.client = client
        self.storage = {}
        self.message = Message(client)
        
    def send(self, message):
        return self.message.send(message)
        
    def receive(self):
        return self.message.receive()
    
    def close(self):
        self.client.close()
