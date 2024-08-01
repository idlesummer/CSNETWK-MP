from pathlib import Path


def run(session, request, command_obj, server):
    storage_path = Path(session.storage["storage_path"])
    
    # Get list of files in client"s storage
    dir_paths = [file_path.name for file_path in storage_path.iterdir() if file_path.is_file()]
    dir_paths = "\n".join(dir_paths) if dir_paths else "[Empty]"
    
    # Send list of files
    return {"status": "OK", "message": f"\n\nServer Directory\n{dir_paths}\n"}


def validator(session, request, command_obj, server):
    if "handle" not in session.storage:
        return {"status": "UnregisteredUserError", "message": "Unregistered user. Please register a handle."}


data = {
    "name": "dir",
    "params": [],
    "run": run,
    "validator": validator,
}
