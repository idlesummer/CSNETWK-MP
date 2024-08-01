# from pathlib import Path


# def run(session, request, command_obj, server):
#     handle = request["params"][0]    
#     session.storage['handle'] = handle
    
#     storage_path = Path(server.storage_path)
#     session.storage['storage_path'] = str(storage_path)
    
#     print(f"Server: Used client storage of '{handle}'")
#     return {"status": "OK", "message": f"Welcome {handle}!"}


# def validator(session, request, command_obj, server):
#     handle = request["params"][0]
#     storage_path = Path(server.storage_path) / handle
#     existing_handle = storage_path.stem
    
#     if storage_path.exists() and handle != existing_handle:
#         return {"status": "LoginError", "message": "Login failed. Handle or alias does not exist."}


# data = {
#     'name': 'login',
#     'options': ["handle"],
#     'run': run,
#     'validator': validator,
# }
