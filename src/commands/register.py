from pathlib import Path


def run(interaction, commander):
    handle = interaction.options[0]
    session = interaction.session
    session.set_handle(handle)
    
    storage_path = Path(commander.data_path) / handle
    session.set_storage_path(str(storage_path))
    storage_path.mkdir(parents=True, exist_ok=True)

    print(f"Server: Created new client storage for '{handle}'")
    session.client.send(f'DISPLAY Welcome {handle}!'.encode())


def validator(interaction, command_obj, commander):
    handle = interaction.options[0]
    handle_path = (Path(commander.data_path) / handle)
    
    if handle_path.exists():
        message = 'DISPLAY Error: Registration failed. Handle or alias already exists.'
        interaction.client.send(message.encode())
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
