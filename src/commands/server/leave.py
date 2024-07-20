from pathlib import Path


def run(session, request, command_obj, commander):
    session.send({'msg': 'Connection closed. Thank you!'})
    session.close()
    print(f"Server> Client has disconnected.")
    return True
    

data = {
    'name': 'leave',
    'run': run,
}
