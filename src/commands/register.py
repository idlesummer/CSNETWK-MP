from pathlib import Path


def run(interaction, commander):
    handle = interaction.options[0]
    session = interaction.session

    if session.register(handle):
        print(f"Server: Created new client storage for '{handle}'")
        session.conn.send(f'DISPLAY Welcome {handle}!'.encode())
        
    else:
        session.conn.send(f'Error: DISPLAY Welcome {handle}!'.encode())
        

    # session.set_handle(handle)
    
    # storage_path = Path(commander.data_path) / handle
    # session.set_storage_path(str(storage_path))
    # storage_path.mkdir(parents=True, exist_ok=True)



def validator(interaction, command_obj, commander):
    handle = interaction.options[0]
    handle_path = (Path(commander.data_path) / handle)
    
    if handle_path.exists():
        message = 'DISPLAY Error: Registration failed. Handle or alias already exists.'
        interaction.conn.send(message.encode())
        return True
    
    return False


data = {
    'name': 'register',
    'options': {
        'handler': 'string',
    },
    'run': run,
    'validator': validator,
}
