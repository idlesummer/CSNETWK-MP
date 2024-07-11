from pathlib import Path


def run(interaction, commander):
    client = interaction.client
    command_objs = commander.command_objs
    command_syntax = []
    
    for i, command_name in enumerate(command_objs):
        options_obj = command_objs[command_name]['options']
        options_str = f'<{'> <'.join(options_obj)}>' if len(options_obj) else ''
        command_syntax.append(f'[{i+1}] /{command_name} {options_str}')
    
    client.send(f'DISPLAY \nCommand List\n{'\n'.join(command_syntax)}\n'.encode())


data = {
    'name': '?',
    'run': run,
}