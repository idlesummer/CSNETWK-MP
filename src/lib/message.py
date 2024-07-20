import json


class Message:
    
    def __init__(self, message='', invalid_request=False, disconnected=False, timed_out=False):
        self.message = message
        self.invalid_request = invalid_request
        self.disconnected = disconnected
        self.timed_out = timed_out
        self.data = {}
        
        try: 
            message = message.replace('\\"', '"')
            self.data = json.loads(message)        
    
        except:
            self.invalid_request = True
            self.disconnected = True
            
        self.data.setdefault('args', [])
        self.data.setdefault('cmd', '')
        self.data.setdefault('status', '')
        self.data.setdefault('msg', '')
        
    @property
    def args(self):
        return self.data['args']
    
    def __str__(self):
        return str(self.__dict__)
