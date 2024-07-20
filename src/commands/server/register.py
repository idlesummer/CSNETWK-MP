from pathlib import Path


def run(session, request, commander):       
    handle = request.args[0]    
    session.data['handle'] = handle
    
    storage_path = Path(commander.data_path) / handle
    session.data['storage_path'] = str(storage_path)
    storage_path.mkdir(exist_ok=True)
    
    print(f"Server: Created new client storage for '{handle}'")
    session.send({'msg': f'Welcome {handle}!'})


def validator(session, request, commander):
    handle = request.args[0]
    storage_path = Path(commander.data_path) / handle
    return storage_path.exists()


data = {
    'name': 'register',
    'options': {
        'handle': 'string',
    },
    'run': run,
    'validator': validator,
    'validator_message': 'Error: Registration failed. Handle or alias already exists.',
}
