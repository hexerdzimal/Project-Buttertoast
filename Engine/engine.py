import os
import json
from Engine.plugin_Loader import PluginLoader
from UI.BaseUI import BaseUI
from UI.tui import TUI  
from UI.gui import GUI     
from Crypt.cryptomat import Cryptomat   


class Engine:

    def __init__(self):
        """
        Initializes the Engine, loads the configuration, and sets the UI to None initially.
        """
        self.config = self.load_config()
        self.ui = None


    def load_config(self):
        """
        Loads the configuration file from the project root directory.

        Raises:
            FileNotFoundError: If the configuration file does not exist.

        Returns:
            dict: Loaded configuration as a dictionary.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, "config.json")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The configuration file {config_path} was not found.")
        
        with open(config_path, "r") as file:
            config = json.load(file)
        
        return config
    
    
    def select_ui(self):
        """
        Selects the user interface (GUI or TUI) based on the configuration.
        Defaults to TUI if the 'gui' setting is False or not present.
        """
        use_gui = self.config.get("gui", False)  # Default to False (TextUI)
        
        if use_gui:
            self.ui = GUI()
        else:
            self.ui = TUI()


    def start_ui(self):
        """
        Initializes the base user interface and links it to the engine as a controller.
        """
        self.ui = BaseUI()
        self.ui.set_controller(self)  # Pass the Engine as a controller to the UI


    def process_data(self, host, host_bytecode, volume_bytecode, password, output):
        """
        Processes the data, runs the plugin, and returns the result.

        Args:
            host (str): Path to the host file.
            host_bytecode (bytes): Bytecode of the host file.
            volume_bytecode (bytes): Bytecode of the volume file.
            password (str): Password for encryption.
            output (str): Name of the output file.

        Returns:
            dict: A dictionary indicating success or error details.

        Raises:
            Exception: If there is an error during plugin execution or file saving.
        """
        print(f"Processing data: Password={password}, Output={output}")

        try:
            # Load and run the plugin
            plugin = PluginLoader
            poly_bytecode = plugin.load_and_run_plugin(host, volume_bytecode, host_bytecode)

            # Encrypt using Cryptomat
            cryptomat = Cryptomat
            buttertoast = cryptomat.cryptomator(volume_bytecode, poly_bytecode, password)

            # Save the result to a file
            self.save_bytecode_to_file(buttertoast, output)  # Use 'output' as the filename

            return {"status": "File successfully created"}
        except Exception as e:
            print(f"[ERROR] Error during plugin execution: {e}")
            return {"status": "Error", "error_message": str(e)}


    def handle_user_input(self, host, volume, password, output):
        """
        Processes user input from the UI and validates it.

        Args:
            host (str): Path to the host file.
            volume (str): Path to the volume file.
            password (str): Password for encryption.
            output (str): Path to the output file.

        Raises:
            ValueError: If any of the inputs are missing.
            Exception: If there is an error during file processing.

        """
        try:
            # Validate input
            if not host or not volume or not password or not output:
                raise ValueError("All inputs must be provided!")

            # Read the host and volume files as bytecode
            host_bytecode = self.read_file_as_bytecode(host)
            volume_bytecode = self.read_file_as_bytecode(volume)

            # Pass the bytecode data for processing
            result = self.process_data(host, host_bytecode, volume_bytecode, password, output)

            # Display the results to the UI
            self.ui.show_result(result)

        except Exception as e:
            self.ui.show_error(f"Error during processing: {str(e)}")


    def read_file_as_bytecode(self, file_path):
        """
        Reads a file and returns its content as bytecode.

        Args:
            file_path (str): Path to the file.

        Returns:
            bytes: The content of the file as bytecode.

        Raises:
            ValueError: If the file cannot be read.
        """
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading the file '{file_path}': {e}")
        
    def save_bytecode_to_file(self, bytecode: bytes, filename: str):
        """
        Saves the given bytecode to a file.

        Args:
            bytecode (bytes): The data to save.
            filename (str): Name of the output file.

        Raises:
            Exception: If the file cannot be written.
        """
        try:
            with open(filename, 'wb') as file:
                file.write(bytecode)
            print(f"[DEBUG] Bytecode successfully written to the file '{filename}'.")
        except Exception as e:
            print(f"[ERROR] Error saving bytecode to the file '{filename}': {e}")

    

    def start(self):
        """
        Starts the engine, initializes the UI, and links it to the engine.

        Raises:
            Exception: If there is an error during engine initialization or UI startup.
        """
        try:
            self.select_ui()
            self.ui.set_controller(self)  # Links the UI with the Engine
            self.ui.run()
        except Exception as e:
            print(f"Error starting the engine: {e}")
