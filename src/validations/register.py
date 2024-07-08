import os


def validate(interaction, command_obj, commander):
    handle = interaction.options[0]
    handle_exists = os.path.exists(os.path.join(commander.data_path, handle))
    
    if handle_exists:
        message = 'Error: Registration failed. Handle or alias already exists.'
        interaction.client.send(message.encode())
        return True
    
    return False
