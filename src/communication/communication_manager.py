import socket


class CommunicationManager:
    def __init__(self, sock):
        self.sock = sock
    
    def send(self, message):
        try:
            message = message.encode()
            message_length = len(message)
            message_length = int.to_bytes(4, byteorder='big')
            
            # Send the message length
            self.sock.sendall(message_length)
            
            # Send the actual message data
            self.sock.sendall(message)
            
        except Exception as e:
            print(e)
            
    
    def recieve(self):
        try:
            message_length = self.sock.recv(4).decode()
            message_length = int.from_bytes(message_length, byteorder='big')
            message = b''
            
            while len(message) < message_length:
                chunk = self.sock.recv(4096)
                if not chunk:
                    # raise ConnectionError('Client disconnected unexpectedly')
                    message += chunk
                    
            # Parse the message
            message = message.decode()
            return message    
    
        except Exception as e:
            return None
