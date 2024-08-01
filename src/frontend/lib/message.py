import json
import socket


class Message:
    
    def __init__(self, socket):
        self.socket = socket
        
        
    def send(self, message):
        try:
            message_byte = json.dumps(message).encode("utf-8")
            message_length = len(message_byte)
            
            # Send the message length
            self.socket.sendall(message_length.to_bytes(4, byteorder="big"))
            
            # Send the actual message data
            self.socket.sendall(message_byte)
            return { "status": "OK", "message": message_length }
            
        except (TypeError, json.JSONDecodeError, UnicodeEncodeError, socket.error, ConnectionResetError, ConnectionAbortedError, OSError, Exception) as e:
            
            return { "status": type(e).__name__, "message": e }
        
        
    def receive(self):
        try:
            message_length_byte = self.socket.recv(4)
            
            if not message_length_byte:
                raise ConnectionResetError("An existing connection was forcibly closed by the remote host.")
           
            message_length =  int.from_bytes(message_length_byte, byteorder="big")
            message = b""
            
            while len(message) < message_length:
                chunk = self.socket.recv(4096)
                
                if not chunk:
                    raise ConnectionResetError("An existing connection was forcibly closed by the remote host.")
                
                message += chunk
            
            message = message.decode().replace('\\"', '"')
            request = json.loads(message)
            return request
            
        except (json.JSONDecodeError, socket.error, ConnectionResetError, ConnectionAbortedError, OSError, Exception) as e:
            return {"status": type(e).__name__, "message": e}


    def fetch(self, request):
        response = self.send(request)
        
        if response["status"] != "OK":
            return response
               
        response = self.receive()
        return response
        