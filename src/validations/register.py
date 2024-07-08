import os


def validate(interaction, command_obj, commander):
    handle = interaction.options[0]
    handle_exists = os.path.exists(os.path.join(commander.dataPath, handle))
    
    if handle_exists:
        message = 'Error: Registration failed. Please connect to the server first.'
        interaction.client.send(message.encode())
        return False
    
    return True
