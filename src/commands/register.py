from pathlib import Path


def run(interaction, commander):
    handle = interaction.options[0]
    session = interaction.session
    session.set_handle(handle)
    
    storage_path = Path(commander.data_path) / handle
    session.set_storage_path(str(storage_path))
    storage_path.mkdir(parents=True, exist_ok=True)

    print(f"Server: Created new client storage for '{handle}'")
    session.client.send(f'Welcome {handle}!'.encode())


data = {
    'name': 'register',
    'options': {
        'handler': 'string',
    },
    'run': run,
}
