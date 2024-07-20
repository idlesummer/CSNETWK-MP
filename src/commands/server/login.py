from pathlib import Path


def run(session, request, command_obj, commander):       
    handle = request.args[0]    
    session.data['handle'] = handle
    
    storage_path = Path(commander.data_path) / handle
    session.data['storage_path'] = str(storage_path)
    
    print(f"Server: Used client storage of '{handle}'")
    session.send({'msg': f'Welcome {handle}!'})


def validator(session, request, command_obj, commander):
    handle = request.args[0]
    storage_path = Path(commander.data_path) / handle
    return not storage_path.exists()


data = {
    'name': 'login',
    'options': {
        'handle': 'string',
    },
    'run': run,
    'validator': validator,
    'validator_message': 'Error: Login failed. Handle or alias does not exist.',
}
