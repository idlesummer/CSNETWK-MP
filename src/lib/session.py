import json
import socket
from .message import Message


class Session:
    
    def __init__(self, socket):
        self._socket = socket
        self._data = {}

    
    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)
    
    
    def send(self, message):    
        try:
            message_bytestr = json.dumps(message).encode('utf-8')
            message_length = len(message_bytestr).to_bytes(4, byteorder='big')
            
            # Send the message length
            self.socket.sendall(message_length)
            
            # Send the actual message data
            self.socket.sendall(message_bytestr)
            return message_length
            
        except TypeError as e:
            print(f"Server: Error, message must be a dictionary: {e}")
            raise
        
        except json.JSONEncodeError as e:
            print(f"Server: Error encoding message to JSON: {e}")
            raise
            
        except socket.error as e:
            print(f"Server: Connection error while sending: {e}")
            return False
    
            
    def receive(self):
        try:
            message_length = self.socket.recv(4).decode('utf-8')
            message_length = int.from_bytes(message_length, byteorder='big')
            message = b''

            while len(message) < message_length:
                chunk = self.socket.recv(4096)

                if not chunk:
                    raise ConnectionError("Client disconnected before sending full message.")

                message += chunk

            # Parse the message
            message = message.decode()

            # Pass the dictionary to Message object
            return Message(json.loads(message))

        except json.JSONDecodeError as e:
            print(f"Server: Error decoding JSON: {e}")
            raise
        
        except socket.timeout as e:
            print(f"Server: Socket timeout during receive: {e}")
            return Message(disconnected=True, timed_out=True)
        
        except socket.error as e:
            print(f"Server: Socket error during receive: {e}")
            return Message(disconnected=True)

        
    @property
    def socket(self):
        return self._socket
    
    
    @property
    def data(self):
        return self._data
