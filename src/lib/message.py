import json


class Message:
    
    def __init__(self, message='', error_message='', invalid_request=False, disconnected=False, timed_out=False):
        self.message = message
        self.error_message = error_message
        self.invalid_request = invalid_request
        self.disconnected = disconnected
        self.timed_out = timed_out

        self.data = {}
        self.data.setdefault('args', [])
        self.data.setdefault('cmd', '')
        self.data.setdefault('status', '')
        self.data.setdefault('msg', '')
        
        # This doesnt correctly catch JSONDecodeError for some reason
        try: 
            message = message.replace('\\"', '"')
            self.data = json.loads(message)
            
        except: 
            self.invalid_request = True
            
        
    @property
    def args(self):
        return self.data['args']
    
    def __str__(self):
        return str(self.__dict__)
