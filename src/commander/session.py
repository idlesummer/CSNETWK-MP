class Session:
    def __init__(self, server, client, addr):
        self.server = server
        self.client = client
        self.addr = addr
        self.handle = None
        self.storage_path = None
        
    def set_handle(self, handle):
        self.handle = handle

