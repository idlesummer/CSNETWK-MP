class Message:
    
    def __init__(self, data={}, disconnected=False, timed_out=False):
        self._data = data
        self._disconnected = disconnected
        self._timed_out = timed_out
        
        self.data = { }
        self.disconnect = False
        self.timed_out = False

    
    @property
    def data(self):
        return self._data


    @property
    def disconnected(self):
        return self._disconnected
    
    
    @property
    def timed_out(self):
        return self._timed_out
