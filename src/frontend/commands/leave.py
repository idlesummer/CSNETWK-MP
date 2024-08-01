def run(storage, request, command_obj, client):    
    if not storage["connected"]:
        return {"status": "NotConnectedError", "message": "Disconnection failed. Please connect to the server first"}
    
    response = client.message.fetch({"status": "OK", "command": "leave"})
    client.close()
    client.remove()
    
    response["dont_fetch"] = True
    storage["connected"] = False
    return response


data = {
    "name": "leave",
    "params": [],
    "run": run,
}
