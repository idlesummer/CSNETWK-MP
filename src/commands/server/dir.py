from pathlib import Path


def run(session, request, command_obj, commander):
    handle = session.data['handle']
    storage_path = Path(session.data['data_path']) / handle
    
    # Get list of files in client's storage
    dir_paths = [file_path.name for file_path in storage_path.iterdir()]
    dir_paths = '\n'.join(dir_paths) if dir_paths else '[Empty]'
    
    # Send list of files
    session.send({'msg': f'\nServer Directory\n{dir_paths}\n'})


def validator(session, request, command_obj, commander):
    return 'handle' not in session.data


data = {
    'name': 'dir',
    'run': run,
    'validator': validator,
    'validator_message': 'Error: Unregistered user. Please register a handle.',
}
