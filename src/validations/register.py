from pathlib import Path


def validator(interaction, command_obj, commander):
    handle = interaction.options[0]
    handle_path = (Path(commander.data_path) / handle)
    
    if handle_path.exists():
        message = 'Error: Registration failed. Handle or alias already exists.'
        interaction.client.send(message.encode())
        return True
    
    return False
