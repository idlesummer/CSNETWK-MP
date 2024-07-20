from pathlib import Path


def run(session, request, command_obj, commander):
    command_objs = commander.command_objs
    commands_list = []
    
    # for i, command_name in enumerate(command_objs):
    #     options_obj = command_objs[command_name]['options']
    #     options_str = f'<{'> <'.join(options_obj)}>' if len(options_obj) else ''
    #     command_syntax.append(f'[{i+1}] /{command_name} {options_str}')
    
    for i, command_name in enumerate(command_objs):
        options_obj = command_objs[command_name]['options']
        options_str = f'<{'> <'.join(options_obj)}>' if len(options_obj) else ''
        commands_list.append(f'/{command_name} {options_str}')
    
    session.send({'msg': f'\n'.join(commands_list)})


data = {
    'name': '?',
    'run': run,
}
