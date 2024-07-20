import json
import socket
from .message import Message


class Session:
    
    def __init__(self, socket):
        self.socket = socket
        self.data = {}
        self.requested = False
        self.responded = False


    def connect(self, addr):
        self.socket.connect(addr)
        return self.receive()
    
    
    def set_timeout(self, timeout):
        self.socket.settimeout(timeout)
    
    
    def close(self):
        self.socket.close()
    
    
    def send(self, message):    
        try:
            message_bytestr = json.dumps(message).encode('utf-8')
            message_length = len(message_bytestr).to_bytes(4, byteorder='big')
            
            # Send the message length
            self.socket.sendall(message_length)
            
            # Send the actual message data
            self.socket.sendall(message_bytestr)
            return int.from_bytes(message_length, byteorder='big')
            
        except TypeError as e:
            print(f"Error encoding message to JSON, message must be a dictionary: {e}")
            raise

        except socket.error as e:
            print(f"Connection error while sending: {e}")
            return False
    
            
    def receive(self):
        try:
            message_length_byte = self.socket.recv(4)
            message_length = int.from_bytes(message_length_byte, byteorder='big')
            message = b''

            while len(message) < message_length:
                chunk = self.socket.recv(4096)

                if not chunk:
                    raise ConnectionError("Client disconnected before sending full message.")

                message += chunk

            # Parse the message
            message = message.decode()

            # Pass the dictionary to Message object
            return Message(message)

        except json.JSONDecodeError as e:
            return Message(error_message=f'Error decoding JSON: {e}', disconnected=True)
        
        except socket.timeout as e:
            return Message(error_message=f'Socket timeout during receive: {e}', disconnected=True, timed_out=True)
        
        except socket.error as e:
            return Message(error_message=f'Socket error during receive: {e}', disconnected=True)
