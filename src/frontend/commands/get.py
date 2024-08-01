from base64 import b64encode
from pathlib import Path


def run(storage, request, command_obj, client):    
    if not storage["connected"]:
        return {"status": "NotConnectedError", "message": "Not connected to a server."}
    
    filename = request["params"][0]
    
    if not Path(filename).exists():
        return {"status": "FileNotFoundError", "message": "File not found."}
    
    with open(filename, "rb") as file:
        file_bytes= file.read()
        
    request["body"] = b64encode(file_bytes).decode('utf-8')
    return request


data = {
    "name": "store",
    "params": [],
    "run": run,
}
