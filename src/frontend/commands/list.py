from pathlib import Path
from socket import *


def run(storage, request, command_obj, client):  
    command_objs = client.command_objs
    commands_list = []
    
    for i, command_name in enumerate(command_objs):
        params_list = command_objs[command_name]['params']
        params_str = f'<{'> <'.join(params_list)}>' if len(params_list) else ''
        commands_list.append(f'/{command_name} {params_str}')
    
    commands_list.sort()
    request = {"status": "OK", "command": "?", "message": f"\n\nCommands List\n{'\n'.join(commands_list)}\n"}
    
    if not storage["connected"]:
        request["dont_fetch"] = True
        
    return request


data = {
    "name": "?",
    "params": [],
    "run": run,
}
