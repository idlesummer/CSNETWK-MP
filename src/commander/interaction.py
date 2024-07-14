class Interaction:
    def __init__(self, session, message):
        self.session = session
        self.conn = session.conn
        self.message = message
        self.tokens = message.split()
        self.command_name = None
        self.options = None

        if self.is_command():  # This will call the instance method
            self.command_name = self.tokens[0][1:]
            self.options = self.tokens[1:]

    def is_command(self):  # Instance method
        return self.message.startswith('/')
