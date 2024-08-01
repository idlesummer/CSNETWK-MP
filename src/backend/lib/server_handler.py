# Standard package imports
import logging
from pathlib import Path
import threading


# Internal package imports
from .import_file import import_file
from .session import Session


class Server:
    
    def __init__(self, server, commands_path, storage_path):
        self.socket = server
        self.commands_path = commands_path
        self.storage_path = storage_path
        self.command_objs = {}
        
         # Set up logger
        logging.basicConfig(level=logging.INFO, format="\033[92m%(levelname)s:\033[0m %(message)s")
        
        # Start server handler
        logging.info("Starting...")
        logging.info(f"Used storage at '{storage_path}'\n")
        self.load_commands()
        self.handle_sessions()
        
        
    def load_commands(self):        
        for command_path in Path(self.commands_path).glob("*.py"):
            try:
                command_module = import_file(command_path.stem, command_path)
                command_obj = command_module.data
                command_name = command_obj.get("name", None)                                

                # Populate optional properties with default values
                command_obj["params"] = command_obj.get("params", {})
                command_obj["validator"] = command_obj.get("validator", None)

                # Add command object to collection
                self.command_objs[command_name] = command_obj
                logging.info(f"Loaded command '{command_name}' from '{command_path}'")
            
            except (AttributeError, ImportError, OSError) as e:
                logging.error(f"Failed to load command from '{command_path}': {e}")
            
        print("")
        ip, port = self.socket.getsockname()
        logging.info(f"Server is listening on: {ip}:{port}\n")


    def handle_sessions(self): 
        while True:
            # Accept client connections
            logging.info("Waiting for client connections...")
            client, _ = self.socket.accept()
            session = Session(client)

            # Start separate thread
            thread = threading.Thread(target=self.on_connect, args=(session,))
            thread.start()
            
    
    def on_connect(self, session):
        session.storage["server"] = self.socket
        session.storage["storage_path"] = self.storage_path
        
        # Log successful connection
        logging.info("Accepted client connection.")
        
        # Send connection success message
        session.send({"status": "OK", "message": "Connection to the File Exchange Server is successful!"})
        
        # Main session loop
        while True:
            # Wait for client request
            request = session.receive()
            
            if request["status"] != "OK":
                logging.info("A client has disconnected.")
                break

            # Process request
            self.on_request(session, request)
            
    def on_request(self, session, request):
        command_name = request.get("command")
        command_obj = self.command_objs.get(command_name) if command_name else None
        print(command_name)
        try:     
            # Validate request
            if response := self.validate_request(session, request, command_obj):
                return session.send(response)
            
            logging.info(f"Running command '{command_name}'")
            command_run = command_obj["run"]
            response = command_run(session, request, command_obj, self)
            session.send(response)
            
            if command_name == "leave":
                return session.close() # Disconnection message will be watched by request status
        
        except Exception as e:
            # For development
            logging.exception(f"Error: {e}")
            
            # For production
            # logging.error(f"Error: {e}")
         
            
    def validate_request(self, session, request, command_obj):
        
         # Check if command exists
        if command_obj is None:
            return {"status": "CommandError", "message": "Command not found."}
        
        # Check for incorrect argument length
        if command_obj["params"] and len(request["params"]) != len(command_obj["params"]):
            return {"status": "CommandParamsError", "message": "Command parameters do not match or is not allowed."}

        # Command-specific validations
        if command_obj["validator"] and (response := command_obj["validator"](session, request, command_obj, self)):
            return response
