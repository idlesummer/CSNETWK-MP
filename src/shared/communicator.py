import json


class Communicator:
    def __init__(self, socket):
        self.socket = socket
        
    def send(self, message):    
        try:
            message = message.encode('utf-8')
            message_length = len(message).to_bytes(4, byteorder='big')
            
            # Send the message length
            self.socket.sendall(message_length)
            
            # Send the actual message data
            self.socket.sendall(message)
            
        except ConnectionError as e:
            print(f'Server: Error sending message, client disconnected unexpectedly: {e}')
            return None
            
        except (UnicodeEncodeError, OSError) as e:
            print('Server: Error sending message: {e}')
            return None
        
    def receive(self):
        try:
            message_length = self.socket.recv(4).decode('utf-8')
            message_length = int.from_bytes(message_length, byteorder='big')
            message = b''
            
            while len(message) < message_length:
                chunk = self.conn.recv(4096)
                if not chunk:
                    message += chunk
                    
            # Parse the message
            message = message.decode()
            
            # Return parsed message
            return message

        except ConnectionError as e:
            print(f'Server: Error receiving message, client disconnected unexpectedly: {e}')
            return None
        
        except OSError as e:
            print(f'Server: Error receiving message: {e}')
            return None
