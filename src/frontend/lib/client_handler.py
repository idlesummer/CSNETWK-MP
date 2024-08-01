# Standard imports
from base64 import b64decode
import logging
from pathlib import Path
from socket import *

# Internal imports
from .import_file import import_file
from .interaction import Interaction
from .message import Message


class Client:
    
    def __init__(self, commands_path):
        self.commands_path = commands_path
        self.command_objs = {}
        self.storage = {"connected": False}
        self.socket = None
        self.message = None
        
        # Set up logger
        logging.basicConfig(level=logging.INFO, format="\033[92m%(levelname)s:\033[0m %(message)s")
        
        # Start client handler
        logging.info("Client is starting...\n")
        self.load_commands()
        self.handle_session()
     
        
    def load_commands(self):
        for command_path in Path(self.commands_path).glob('*.py'):    
            try:
                command_module = import_file(command_path.stem, command_path)
                command_obj = command_module.data
                command_name = command_obj.get('name', None)
                
                # Populate optional properties with default values
                command_obj['options'] = command_obj.get('options', {})
                command_obj['validator'] = command_obj.get('validator', None)
                
                # Add command object to collection
                self.command_objs[command_name] = command_obj
                logging.info(f"Loaded command '{command_name}' from '{command_path}'")
                
            except (AttributeError, ImportError, OSError) as e:
                logging.error(f"Failed to load command from '{command_path}: {e}'")
        
        print("")
        logging.info("Client is ready!\n")
                

    def handle_session(self):

        # Main session loop
        while True:
            
            # Listen for user commands
            prompt = input("Client> ")
            interaction = Interaction(prompt)
            
            # Create an interaction
            self.on_interaction(interaction)
    
    
    def on_interaction(self, interaction):
        command_name = interaction.command
        command_obj = self.command_objs.get(command_name)
        
        try:
            # Validate interaction syntax
            if message := self.validate_interaction(interaction, command_obj):
                return logging.error(f"Error: {message}")
            
            request = interaction.to_request()

            # Check if client is not connected and command doesn't exist
            if not self.storage["connected"] and command_obj is None:
                request = {"status": "UnknownCommandError", "message": "Command not found."}

            # Otherwise, perform additional request processing if command is special
            elif command_obj is not None:
                command_run = command_obj["run"]
                request = command_run(self.storage, request, command_obj, self)

            # Check if request processing failed            
            if request["status"] != "OK":  
                return logging.error(f"Error: {request["message"]}")
            
            # Fetch a response from the server if fetching is allowed by the special commands
            response = request if request.get("dont_fetch") else self.message.fetch(request)

            # Check if response is ok
            if response["status"] != "OK":
                return logging.error(f"Error: {response["message"]}")

            # Log the message
            print(f"Server> {response["message"]}")
            
            # Download body if there is
            if "body" in response:
                filename = response["message"].split()[-1]
                file_data = b64decode(response["body"])
                            
                with open(Path.cwd() / filename, "wb") as file:
                    file.write(file_data)
            
        except Exception as e:
            # For development
            # logging.exception(f"Error: {e}")
            
            # For production
            logging.error(f"Error: {e}")


    def validate_interaction(self, interaction, command_obj):
        
        # Check command syntax
        if not interaction.is_command():
            return "Invalid command syntax"


    def create(self, client_socket):
        self.socket = client_socket
        self.message = Message(client_socket)


    def remove(self):
        self.socket = None
        self.message = None


    def connect(self, ip, port):
        try:
            self.socket.connect((ip, port))
            response = self.message.receive()
            return response
        
        except Exception as e:
            #  logging.error(f"Error: {e}")
             return {"status": "ConnectingError", "message": "Connection to the Server has failed! Please check IP Address and Port Number."}
             
    
    def close(self):
        self.socket.close()
