def run(session, request, command_obj, server):
    return {"status": "OK", "message": "Connection closed. Thank you!"}


data = {
    "name": "leave",
    "params": [],
    "run": run,
}