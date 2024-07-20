class Interaction:
    
    def __init__(self, prompt):
        self.prompt = prompt
        self.tokens = []
        self.message = ''
        self.command = ''
        self.args = []
 
        if self.is_command():
            self.tokens = prompt.split()
            self.command = self.tokens[0][1:]
            self.args = self.tokens[1:]    
        
    def is_command(self):
        return self.prompt.startswith('/')
    
    
    def to_json(self):
        return {
            'status': 'OK',
            'msg': 'Hello Server!',
            'cmd': self.command,
            'args': self.args,
        }


    def __str__(self):
        return str(self.__dict__)
