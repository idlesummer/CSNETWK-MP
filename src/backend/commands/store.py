from base64 import b64decode
from datetime import datetime
from pathlib import Path


def run(session, request, command_obj, server):          
    filename = request["params"][0]    
    file_data = request["body"]
    
    storage_path = session.storage['storage_path']
    handle = session.storage['handle']
    path = str(Path(storage_path) / filename) 
        
    file_data = b64decode(file_data)
    with open(path, 'wb') as file:
        file.write(file_data)
    
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    return {"status": "OK", "message": f"{handle}<{timestamp}>: Uploaded {filename}"}


def validator(session, request, command_obj, server):   
    handle = session.storage.get("handle")
    storage_path = Path(server.storage_path)
    
    if not storage_path.exists():
        return {"status": "StorageError", "message": "Storage failed. Please register or login first."}


data = {
    "name": "store",
    "params": ["filename"],
    "run": run,
    "validator": validator,
}
