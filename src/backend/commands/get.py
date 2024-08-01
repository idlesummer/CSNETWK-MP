from base64 import b64encode
from pathlib import Path


def run(session, request, command_obj, server):     
    filename = request["params"][0]
    storage_path = session.storage['storage_path']
    path = Path(storage_path) / filename
   
    if not path.exists():
        return {"status": "FileNotFoundError", "message": "File not found."}
    
    path = str(path)
    with open(path, "rb") as file:
        file_bytes = file.read()
        
    response = {"status": "OK", "message": f"File received from Server: {filename}", "body": b64encode(file_bytes).decode('utf-8')}
    return response


def validator(session, request, command_obj, server):
    if "handle" not in session.storage:
        return {"status": "UnregisteredUserError", "message": "Unregistered user. Please register a handle."}


data = {
    "name": "get",
    "params": ["filename"],
    "run": run,
}
