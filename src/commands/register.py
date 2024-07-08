def run(interaction, commander):
    handle = interaction.options[0]
    print('Command:', interaction.command_name)
    print('Handle:', handle)
    return True

data = {
    'name': 'register',
    'options': {
        'handler': 'string',
    },
    'run': run,
}