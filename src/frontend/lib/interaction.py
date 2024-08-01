class Interaction:
    
    def __init__(self, prompt):
        self.prompt = prompt
        self.tokens = []
        self.message = ""
        self.command = ""
        self.args = []
        
        if self.is_command():
            self.tokens = prompt.split()
            self.command = self.tokens[0][1:]
            self.args = self.tokens[1:]    
   
        
    def is_command(self):
        return self.prompt.startswith("/")
   
    
    def __str__(self):
        return str(self.__dict__)
    
    
    def to_request(self):
        return {
            "command": self.command,
            "params": self.args,
            "status": "OK",
            "body": None,
        }
