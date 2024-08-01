from socket import *


def run(storage, request, command_obj, client):
    if len(request["params"]) != 2:
        return {"status": "CommandParamsError", "message": "Command parameters do not match or is not allowed."}
    
    if storage["connected"]:
        return {"status": "AlreadyConnectedError", "message": "Already connected to a server."}
    
    ip, port = request["params"]
    
    response = {"status": "OK", "message": ""}
    
    # Check if port is a valid integer
    try: port = int(port)
    except Exception as e:
        response = {"status": "ConnectingError", "message": "Connection to the Server has failed! Please check IP Address and Port Number."}

    # If port number is valid
    if response["status"] == "OK":
        client.create(socket(AF_INET, SOCK_STREAM))
        response = client.connect(ip, port)
    
    # If connection is valid
    if response["status"] == "OK":
        storage["connected"] = True

    response["dont_fetch"] = True
    return response


data = {
    "name": "join",
    "params": ["server_ip_add", "port"],
    "run": run,
}
