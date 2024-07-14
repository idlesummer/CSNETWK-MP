from pathlib import Path


class Session:
    def __init__(self, server, conn, data_path):
        self.server = server
        self.conn = conn
        self.data_path = data_path
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
    
    def send(self, message):
        try:
            message = message.encode()
            length = len(message)
            
            # Send the message length
            self.conn.sendall(length)
            
            # Send the actual message data
            self.conn.sendall(message)
        except Exception as e:
            print(e)
        
    
    def receive(self):
        length = self.conn.recv(4).decode()
        
        message_length = int.from_bytes(length, byteorder='big')
        message = b''
        
        while len(message) < message_length:
            chunk = self.conn.recv(4096)
            if not chunk:
                # raise ConnectionError('Client disconnected unexpectedly')
                message += chunk
                
            # Parse the message
            message = message.decode()
        
        # Return parsed message
        return message
