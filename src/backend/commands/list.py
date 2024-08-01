from pathlib import Path


def run(session, request, command_obj, server):
    command_objs = server.command_objs
    commands_list = []
    
    for i, command_name in enumerate(command_objs):
        params_list = command_objs[command_name]['params']
        params_str = (f'<{'> <'.join(params_list)}>' if len(params_list) else '').strip()
        commands_list.append(f'/{command_name} {params_str}')
    
    commands = request["message"].strip().split("\n")[1:]
    commands_list.extend(commands)
    commands_list = list(set(commands_list))
    commands_list.sort()
    
    return {"status": "OK", "message": f"\n\nCommands List\n{'\n'.join(commands_list)}\n"}


data = {
    "name": "?",
    "params": [],
    "run": run,
}
