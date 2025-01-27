# Buttertoast Copyright (C) 2024 Matthias Ferstl, Fabian Kozlowski, Stefan Leippe, Malte Muthesius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For more information, contact: mail@matthias-ferstl.de


import os
import json
from buttertoast.Utilities.try_tchuntng import run_tchuntng, check_tchuntng
from buttertoast.Engine.plugin_Loader import PluginLoader
from buttertoast.UI.CLI import CLI
from buttertoast.UI.tui import TUI  
from buttertoast.UI.gui import GUI     
from buttertoast.Crypt.cryptomat import Cryptomat


class Engine:

    CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

    def __init__(self, event_manager):
        self.event_manager = event_manager
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

        if not os.path.exists(self.CONFIG_PATH):
            raise FileNotFoundError(f"The configuration file {self.CONFIG_PATH} was not found.")
        
        with open(self.CONFIG_PATH, "r") as file:
            config = json.load(file)
        
        return config
    
    def save_config(self):
        """
        Saves configuration to a config.json file.
        """

        with open(self.CONFIG_PATH, "w") as file:
            json.dump(self.config, file, indent=4)
    
    def select_ui(self):
        """
        Selects the user interface (GUI or TUI) based on the configuration.
        """
        use_gui = self.config.get("gui", False)
        if use_gui:
            self.ui = GUI(self, self.event_manager)  
        else:
            self.ui = TUI(self, self.event_manager)  

    def start_ui(self):
        """
        Starts the already selected UI.
        """
        if self.ui is None:
            raise RuntimeError("No UI selected. Call 'select_ui()' first.")
        self.ui.run()

    def process_data(self, host, host_bytecode, volume_bytecode, password, output):
        """
        Processes user input from the UI, validates it, and performs data processing.

        Args:
            host (str): Path to the host file.
            volume (str): Path to the volume file.
            password (str): Password for encryption.
            output (str): Path to the output file.

        Raises:
            ValueError: If any of the inputs are missing.
            Exception: If there is an error during plugin execution or file saving.
        """
        try:

            # Extract file extension from host file
            extension = self.get_file_extension(host)

            # Load and run the plugin, passing the extension
            plugin = PluginLoader(ui=self.ui)
            poly_bytecode = plugin.load_and_run_plugin(volume_bytecode, host_bytecode, extension)
            if not poly_bytecode:
                return

            # Perform encryption using Cryptomat
            cryptomat = Cryptomat(ui=self.ui)
            buttertoast = cryptomat.cryptomator(volume_bytecode, poly_bytecode, password)

            if buttertoast is None:
                return

            # Save the result to a file, cut old fileextension if neccessary
            if '.' in output and os.path.splitext(output)[1]:  
                output = os.path.splitext(output)[0]
            outputfile = output + '.' + extension
            self.save_bytecode_to_file(buttertoast, outputfile)

            # Display success message
            check = self.config.get("check", False)
            if not check:

                self.ui.display_message(f"File {os.path.basename(outputfile)} successfully created", "info")
                return

            run_tchuntng(outputfile, self.ui)
            return

        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error during processing: {str(e)}", "error")


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
            # Display debug message to UI
            self.ui.display_message(f"Bytecode successfully written to the file '{filename}'.", "verbose")
        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error saving bytecode to the file '{filename}': {e}", "error")

    def get_file_extension(self, file_path):
        """
        Returns the extension of the file (e.g., 'txt' or 'jpg').

        Args:
            file_path (str): Path to the file.

        Returns:
            str: The file extension without the leading dot (e.g., 'txt').
        """
        _, extension = os.path.splitext(file_path)
        return extension.lstrip('.')  # Removes the leading dot

    def start(self):
        """
        Starts the engine, registers the handler, initializes the UI, and links it to the engine.

        Raises:
            Exception: If there is an error during engine initialization or UI startup.
        """
        # register handler
        self.event_manager.register_event("process_data", self.on_process_data)
        self.event_manager.register_event("list_data", self.on_list_data)
        self.event_manager.register_event("change_ui", self.on_change_ui)
        self.event_manager.register_event("change_verbose", self.on_change_verbose)
        self.event_manager.register_event("change_check", self.on_change_check)

        try:
            self.select_ui()
            self.ui.run()
        except Exception as e:
            # Display error message to UI
            print(f"Error starting the engine: {e}", "error")
            self.ui.display_message(f"Error starting the engine: {e}", "error")

    def on_process_data(self, data):
        """
        Event handler for the 'process_data' event. Also used if tool is runned as CLI

        Args:
            data (dict): Data passed from the UI.
        """

        try:
            host = data["host"]
            volume = data["volume"]
            password = data["password"]
            output = data["output"]

            # Read files and start processing
            host_bytecode = self.read_file_as_bytecode(host)
            volume_bytecode = self.read_file_as_bytecode(volume)
            self.process_data(host, host_bytecode, volume_bytecode, password, output)
            return

        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error: {str(e)}", "error")


    def process_data_cli(self, data, verbose):
        """
        Event handler for the 'process_data' event when the tool is run in CLI mode.

        Args:
            data (dict): Data passed from the CLI.
            verbose (bool): Flag to enable verbose output.
        """
        self.ui = CLI(verbose)
        if verbose:
            print("Verbose mode enabled.")
            print("Starting the processing of data in CLI mode...")

        try:
            host = data["host"]
            volume = data["volume"]
            password = data["password"]
            output = data["output"]

            if verbose:
                print(f"Host file: {host}")
                print(f"Volume file: {volume}")
                print(f"Password: {password}")
                print(f"Output file: {output}")

            # Read files and start processing
            host_bytecode = self.read_file_as_bytecode(host)
            volume_bytecode = self.read_file_as_bytecode(volume)

            if verbose:
                print(f"Read host file: {host}")
                print(f"Read volume file: {volume}")

            self.process_data(host, host_bytecode, volume_bytecode, password, output)

            if verbose:
                print(f"Processing complete. Output saved to {output}")

        except Exception as e:
            # Handle errors and output to the console
            print(f"Error during processing: {str(e)}")

    def on_list_data(self, _):
        try:
            plugin_loader = PluginLoader(directory="plugins", ui=self.ui)  # Pass the UI instance here
            plugin_loader.list_plugins()  
        except Exception as e:
            print(f"Error listing plugins: {e}")


    def on_change_ui(self, _):
        """
        Event handler for the 'change_ui' event.
        Toggles the value of the 'gui' parameter in the config.json.
        """
        try:
            # Get the current value of 'gui' and toggle it
            current_gui = self.config.get("gui", False)
            self.config["gui"] = not current_gui

            # Save the updated configuration
            self.save_config()

            # Output confirmation message
            new_value = "enabled" if self.config["gui"] else "disabled"
            self.ui.display_message(f"GUI has been {new_value}.", "verbose")

            
            self.ui.display_message("Please manually restart the program to apply changes.", "info")

        except Exception as e:
            self.ui.display_message(f"Error while changing UI: {e}", "error")

    def on_change_verbose(self, _):
        """
        Event handler for the 'change_verbose' event.
        Toggles the value of the 'verbose' parameter in the config.json.
        """
        try:
            # Toggle the value of 'verbose'
            self.config["verbose"] = not self.config.get("verbose", False)

            # Save the updated configuration
            self.save_config()

            # Output confirmation message
            new_value = "enabled" if self.config["verbose"] else "disabled"
            self.ui.display_message(f"Verbose has been {new_value}.", "info")
            self.ui.display_message(f"Verbose has been {new_value}.", "verbose")
            self.load_config()
        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error toggling the 'verbose' value: {e}", "error")

    def on_change_check(self, _):
        """
        Event handler for the 'change_check' event.
        Toggles the value of the 'check' parameter in the config.json, but only
        if 'tchuntng' is available in the PATH.
        """
        try:
            # Check if tchuntng is available
            if not check_tchuntng():
                self.ui.display_message(f"'tchuntng' is not available in the PATH or is not executable.", "error")
                return

            # Toggle 'check' value
            self.config["check"] = not self.config.get("check", False)

            # save config
            self.save_config()

           # Output confirmation message
            new_value = "enabled" if self.config["check"] else "disabled"
            self.ui.display_message(f"Auto-check has been {new_value}.", "info")
            self.ui.display_message(f"Checking of generated polyglot has been {new_value}.", "verbose")
            self.load_config()

        except Exception as e:
            # Fehlermeldung ausgeben
            self.ui.display_message(f"Error toggling the 'check' value: {e}", "error")


    