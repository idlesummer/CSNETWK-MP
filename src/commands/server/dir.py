from pathlib import Path


def run(session, request, commander):
    session.data['handle'] = 'Alice'
    storage_path = Path(session.data['data_path']) / session.data['handle']
    
    # Get list of files in client's storage
    dir_paths = [file_path.name for file_path in storage_path.iterdir()]
    dir_paths = '\n'.join(dir_paths) if dir_paths else '[Empty]'
    
    # Send list of files
    session.send({'msg': f'\nServer Directory\n{dir_paths}\n'})


data = {
    'name': 'dir',
    'run': run,
}
