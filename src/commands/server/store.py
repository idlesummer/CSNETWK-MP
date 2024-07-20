from datetime import datetime
from pathlib import Path
from base64 import b64decode

def run(session, request, command_obj, commander):       
    filename = request.args[0]    
    file_data = request.args[1]
    file_content = b64decode(file_data)
    
    storage_path = session.data['storage_path']
    handle = session.data['handle']
    path = str(Path(storage_path) / filename) 
        
    with open(path, 'wb') as file:
        file.write(file_content)
    
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    session.send({'msg': f'{handle}<{timestamp}>: Uploaded {filename}'})


def validator(session, request, command_obj, commander):
    return 'handle' not in session.data


data = {
    'name': 'store',
    'options': {
        'filename': 'string',
        'file-data': 'string',
    },
    'run': run,
    'validator': validator,
    'validator_message': 'Error: Please register or login first.',
}
