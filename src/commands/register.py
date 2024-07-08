import os


def run(interaction, commander):
    handle = interaction.options[0]
    session = interaction.session
    session.set_handle(handle)
    
    storage_path = os.path.join(commander.data_path, handle)
    session.storage_path = storage_path
    print(storage_path)
    os.mkdir(storage_path)
    
    session.client.send(f'Welcome {handle}!'.encode())


data = {
    'name': 'register',
    'options': {
        'handler': 'string',
    },
    'run': run,
}
