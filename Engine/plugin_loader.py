import importlib
import os
import sys

class PluginLoader:
    """
    A class responsible for loading and running plugins based on file extensions.
    It scans a specified directory for plugin files, loads them dynamically,
    and executes the plugin's main function.
    """




    def __init__(self, directory="plugins"):
        """
        Initializes the PluginLoader with a specified directory where the plugins are located.

        Args:
            directory (str): The directory to search for plugin files. Default is "plugins".
        """
        self.directory = directory  # Directory where plugins are located  




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
        print(f"[DEBUG] Trying to load the plugin for extension '{extension}'...")

        plugin_name = self.get_plugin_name(extension)
        print(f"[DEBUG] Found file extension: '{extension}', Plugin name: '{plugin_name}'")

        # Add the plugin directory to sys.path to locate the plugins
        sys.path.insert(0, self.directory)

        try:
            # Try importing the plugin module
            print(f"[DEBUG] Attempting to import plugin '{plugin_name}' and load the class...")
            plugin_module = importlib.import_module(plugin_name)
            class_name = extension.capitalize()  # Capitalize the class name based on convention
            plugin_class = getattr(plugin_module, class_name)

            # Create an instance of the plugin class and run the 'run' method
            print(f"[DEBUG] Creating an instance of '{plugin_class.__name__}'...")
            plugin_instance = plugin_class()
            print(f"[DEBUG] Running the 'run' method of '{plugin_class.__name__}'...")
            poly_byte = plugin_instance.run(volume_byte, host_byte)  # Pass 'host' and 'volume' as bytecode data

            print(f"[DEBUG] '{plugin_class.__name__}' executed successfully.")
            return poly_byte

        except (ModuleNotFoundError, AttributeError) as e:
            print(f"[ERROR] Error loading plugin '{plugin_name}': {e}")
        except Exception as e:
            print(f"[ERROR] Error executing the plugin: {e}")
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
            print(f"[ERROR] Plugin directory '{self.directory}' not found.")
            return available_plugins

        print(f"Available plugins in the directory '{self.directory}':")
        for filename in os.listdir(self.directory):
            # Check if the file starts with "btp_" and ends with ".py", excluding __init__.py
            if filename.startswith("btp_") and filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]  # Remove the ".py" extension
                try:
                    print(f"{plugin_name}")
                except Exception as e:
                    print(f"[ERROR] Error loading plugin '{plugin_name}': {e}")
        
        return available_plugins
    
