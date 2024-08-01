def run(session, request, command_obj, server):
    handle = session.storage.get("handle")
    return {"status": "OK", "message": f"Currently registered as {handle}."}


def validator(session, request, command_obj, server):
    handle = session.storage.get("handle")
    
    if not handle:
        return {"status": "UnregisteredUserError", "message": "Unregistered user. Please register a handle."}


data = {
    'name': 'user',
    'options': ["handle"],
    'run': run,
    'validator': validator,
}
