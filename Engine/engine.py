import os
import sys
import json
from Engine.plugin_Loader import PluginLoader
from UI.BaseUI import BaseUI
from UI.TUI import TUI  
from UI.GUI import GUI     
from Crypt.cryptomat import Cryptomat


def restart_program():
        """Startet das aktuelle Python-Programm neu."""
        try:
            print("Programm wird neu gestartet...")
            python = sys.executable
            os.execl(python, python, *sys.argv)
        except Exception as e:
            print(f"Fehler beim Neustarten: {e}")
            sys.exit(1)
   

class Engine:

    def __init__(self, event_manager):
        self.event_manager = event_manager
        self.config = self.load_config()
        self.ui = None

        # Event-Handler registrieren
        self.event_manager.register_event("process_data", self.on_process_data)
        self.event_manager.register_event("list_data", self.on_list_data)
        self.event_manager.register_event("change_ui", self.on_change_ui)
        self.event_manager.register_event("change_verbose", self.on_change_verbose)
        self.event_manager.register_event("change_language", self.on_change_language)

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
    
    def save_config(self):
        """
        Speichert die geänderte Konfiguration zurück in die Konfigurationsdatei.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, "config.json")
        
        with open(config_path, "w") as file:
            json.dump(self.config, file, indent=4)
    
    def select_ui(self):
        """
        Selects the user interface (GUI or TUI) based on the configuration.
        """
        use_gui = self.config.get("gui", False)
        if use_gui:
            self.ui = GUI(self.event_manager)  
        else:
            self.ui = TUI(self.event_manager)  

    def start_ui(self):
        """
        Starts the already selected UI.
        """
        if self.ui is None:
            raise RuntimeError("No UI selected. Call 'select_ui()' first.")
        self.ui.run()

    def process_data(self, host, host_bytecode, volume_bytecode, password, output_filename):
        """
        Processes the data, runs the plugin, and returns the result.

        Args:
            host (str): Path to the host file.
            host_bytecode (bytes): Bytecode of the host file.
            volume_bytecode (bytes): Bytecode of the volume file.
            password (str): Password for encryption.
            output_filename (str): Name of the output file.

        Returns:
            dict: A dictionary indicating success or error details.

        Raises:
            Exception: If there is an error during plugin execution or file saving.
        """
        try:
            # Extract file extension from host file
            extension = self.get_file_extension(host)

            # Load and run the plugin, passing the extension
            plugin =PluginLoader(ui=self.ui)
            poly_bytecode = plugin.load_and_run_plugin(volume_bytecode, host_bytecode, extension)

            # Perform encryption using Cryptomat
            cryptomat = Cryptomat(ui=self.ui)
            buttertoast = cryptomat.cryptomator(volume_bytecode, poly_bytecode, password)

            if buttertoast is None:
                return {"status": "Oops, something went wrong! Check log for more information"}

            # Save the result to a file
            _, file_extension = os.path.splitext(host)
            outputfile = output_filename + file_extension
            self.save_bytecode_to_file(buttertoast, outputfile)

            return {"status": "File " + os.path.basename(outputfile) +" successfully created"}

        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error during plugin execution: {e}", "error")
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
            self.ui.display_message(result["status"], "info")

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
        Starts the engine, initializes the UI, and links it to the engine.

        Raises:
            Exception: If there is an error during engine initialization or UI startup.
        """
        try:
            self.select_ui()
            self.ui.run()
        except Exception as e:
            # Display error message to UI
            print(f"Error starting the engine: {e}", "error")
            self.ui.display_message(f"Error starting the engine: {e}", "error")

    def on_process_data(self, data):
        """
        Event-Handler für das 'process_data'-Event.

        Args:
            data (dict): Daten, die von der UI übergeben wurden.
        """
        try:
            host = data["host"]
            volume = data["volume"]
            password = data["password"]
            output = data["output"]

            # Dateien einlesen und Verarbeitung starten
            host_bytecode = self.read_file_as_bytecode(host)
            volume_bytecode = self.read_file_as_bytecode(volume)
            result = self.process_data(host, host_bytecode, volume_bytecode, password, output)

            # Ergebnis anzeigen
            self.ui.display_message(result["status"], "info")

        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Fehler: {str(e)}", "error")

    def on_list_data(self, _):
        try:
            plugin_loader = PluginLoader(directory="plugins", ui=self.ui)  # Hier übergibst du die UI-Instanz
            plugin_loader.list_plugins()  # Diese Methode listet die Plugins
        except Exception as e:
            print(f"Fehler beim Auflisten der Plugins: {e}")

    def on_change_ui(self, _):
        """
        Event handler for the 'change_ui' event.
        Toggles the value of the 'gui' parameter in the config.json.
        """
        try:
            # Toggle the value of 'gui'
            self.config["gui"] = not self.config.get("gui", False)

            # Save the updated configuration
            self.save_config()

            # Output confirmation message
            new_value = "enabled" if self.config["gui"] else "disabled"
            self.ui.display_message(f"GUI has been {new_value}.", "info")
            restart_program()
        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error toggling the 'gui' value: {e}", "error")

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
            restart_program()
        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error toggling the 'verbose' value: {e}", "error")

    def on_change_language(self, _):
        """
        Event handler for the 'change_language' event.
        Sets the value of the 'language' parameter in the config.json.
        """
        try:
            # Change language logic can be implemented here
            self.ui.display_message("Language has been changed.", "info")
            restart_program()
        except Exception as e:
            # Display error message to UI
            self.ui.display_message(f"Error toggling the 'language' value: {e}", "error")

    