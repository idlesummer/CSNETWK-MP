import logging
from pathlib import Path


def run(session, request, command_obj, server):       
    handle = request["params"][0]    
    session.storage["handle"] = handle
    storage_path = Path(server.storage_path) / handle
    
    storage_path.mkdir(exist_ok=True)
    session.storage["storage_path"] = str(server.storage_path)
    
    logging.info(f"Server: Created new client storage for '{handle}'")
    return {"status": "OK", "message": f"Welcome {handle}!"}


def validator(session, request, command_obj, server):
    handle = request["params"][0]
    storage_path = Path(server.storage_path) / handle
    
    if storage_path.exists():
        return {"status": "RegisteredUserError", "message": "Registration failed. Handle or alias already exists."}


data = {
    "name": "register",
    "params": ["handle"],
    "run": run,
    "validator": validator,
}
