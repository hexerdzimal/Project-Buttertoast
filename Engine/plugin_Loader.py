import importlib
import os
import sys

class PluginLoader:
    """
    A class responsible for loading and running plugins based on file extensions.
    It scans a specified directory for plugin files, loads them dynamically,
    and executes the plugin's main function.
    """

    def __init__(self, directory="plugins", ui=None):
        """
        Initializes the PluginLoader with a specified directory where the plugins are located
        and an optional UI to display messages.

        Args:
            directory (str): The directory to search for plugin files. Default is "plugins".
            ui (UI): Optional UI instance to display messages. If None, messages won't be displayed.
        """
        self.directory = directory  # Directory where plugins are located
        self.ui = ui  # UI instance for displaying messages

    def get_plugin_name(self, extension):
        """
        Generates the plugin name based on the file extension.

        Args:
            extension (str): The file extension.

        Returns:
            str: The plugin name, e.g., "btp_txt".
        """
        return f"btp_{extension}"

    def load_and_run_plugin(self, volume_byte, host_byte, extension):
        """
        Loads and runs the plugin based on the file extension.

        Args:
            host_name (str): The name of the host file.
            volume_byte (bytes): The bytecode data of the volume.
            host_byte (bytes): The bytecode data of the host.
            extension (str): The file extension.

        Returns:
            bytes: The processed bytecode after running the plugin.
        """
        if self.ui:
            self.ui.display_message(f"Trying to load the plugin for extension '{extension}'...", "verbose")
        
        plugin_name = self.get_plugin_name(extension)
        
        if self.ui:
            self.ui.display_message(f"Found file extension: '{extension}', Plugin name: '{plugin_name}'", "verbose")

        # Add the plugin directory to sys.path to locate the plugins
        sys.path.insert(0, self.directory)

        try:
            if self.ui:
                self.ui.display_message(f"Attempting to import plugin '{plugin_name}' and load the class...", "verbose")
            
            # Try importing the plugin module
            plugin_module = importlib.import_module(plugin_name)
            class_name = 'Filetype'
            plugin_class = getattr(plugin_module, class_name)

            # Create an instance of the plugin class and run the 'run' method
            if self.ui:
                self.ui.display_message(f"Creating an instance of '{plugin_class.__name__}'...", "verbose")
            
            plugin_instance = plugin_class()
            if self.ui:
                self.ui.display_message(f"Running the 'run' method of '{plugin_class.__name__}'...", "verbose")
            
            poly_byte = plugin_instance.run(volume_byte, host_byte)  # Pass 'host' and 'volume' as bytecode data

            if self.ui:
                self.ui.display_message(f"'{plugin_class.__name__}' executed successfully.", "verbose")
            
            return poly_byte

        except (ModuleNotFoundError, AttributeError) as e:
            if self.ui:
                self.ui.display_message(f"[ERROR] Error loading plugin '{plugin_name}': {e}", "error")
        except Exception as e:
            if self.ui:
                self.ui.display_message(f"[ERROR] Error executing the plugin: {e}", "error")
        finally:
            # Remove the plugin directory from sys.path after execution
            sys.path.pop(0)

    def list_plugins(self):
        """
        Lists all available plugins in the specified directory, filtering for files that 
        follow the naming convention "btp_<extension>.py".

        Returns:
            list: A list of plugin names (without extensions) found in the directory.
        """
        available_plugins = []
        
        if not os.path.exists(self.directory):
            if self.ui:
                self.ui.display_message(f"[ERROR] Plugin directory '{self.directory}' not found.", "error")
            return available_plugins

        if self.ui:
            self.ui.display_message(f"Available plugins in the directory '{self.directory}':", "info")
        
        for filename in os.listdir(self.directory):
            # Check if the file starts with "btp_" and ends with ".py", excluding __init__.py
            if filename.startswith("btp_") and filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]  # Remove the ".py" extension
                try:
                    if self.ui:
                        self.ui.display_message(f"{plugin_name}", "info")
                except Exception as e:
                    if self.ui:
                        self.ui.display_message(f"[ERROR] Error loading plugin '{plugin_name}': {e}", "error")
        
        return available_plugins

