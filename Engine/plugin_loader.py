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
    
    def get_extension(self, filename):
        """
        Extracts the file extension from the given filename.

        Args:
            filename (str): The name of the file to extract the extension from.

        Returns:
            str: The file extension (without the leading dot).
        """
        _, extension = os.path.splitext(filename)
        return extension[1:]  # Removes the dot from the extension
    
    def get_plugin_name(self, extension):
        """
        Generates the plugin name based on the file extension.

        Args:
            extension (str): The file extension to generate the plugin name.

        Returns:
            str: The plugin name, formatted as "btp_<extension>".
        """
        return f"btp_{extension}"
    
    def load_and_run_plugin(self, host_name, volume_byte, host_byte):
        """
        Loads and runs the plugin based on the given filename, passing the volume and host bytecode data.

        Args:
            filename (str): The plugin file to load.
            volume (bytes): The bytecode data of the volume.
            host (bytes): The bytecode data of the host.

        Returns:
            bytes: The processed bytecode after running the plugin.
            
        Raises:
            Exception: If there's an error during plugin loading or execution.
        """
        print(f"[DEBUG] Trying to load the plugin for file '{host_name}'...")
        
        # Get file extension and plugin name
        extension = self.get_extension(host_name)
        plugin_name = self.get_plugin_name(extension)
        print(f"[DEBUG] Found file extension: '{extension}', Plugin name: '{plugin_name}'")
        
        # Add the plugin directory to sys.path to locate plugins
        sys.path.insert(0, self.directory)
        
        try:
            # Try importing the plugin module
            print(f"[DEBUG] Attempting to import plugin '{plugin_name}' and load the class...")
            plugin_module = importlib.import_module(plugin_name)
            class_name = extension.capitalize()  # Capitalize the class name to match convention
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
        loaded_plugins = []
        
        if not os.path.exists(self.directory):
            print(f"[ERROR] Plugin directory '{self.directory}' not found.")
            return loaded_plugins

        print(f"Available plugins in the directory '{self.directory}':")
        for filename in os.listdir(self.directory):
            # Check if the file starts with "btp_" and ends with ".py", excluding __init__.py
            if filename.startswith("btp_") and filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]  # Remove the ".py" extension
                try:
                    print(f"{plugin_name}")
                except Exception as e:
                    print(f"[ERROR] Error loading plugin '{plugin_name}': {e}")
        
        return loaded_plugins
    
    def test_plugin(self, filename):
        """
        Loads and tests a plugin based on the provided file. This is used to test a plugin
        in isolation to ensure it runs correctly.

        Args:
            filename (str): The plugin file to test.
            
        Raises:
            Exception: If there is an error during plugin loading or execution.
        """
        print(f"[DEBUG] Testing the plugin for file '{filename}'.")

        # Get file extension and plugin name
        extension = self.get_extension(filename)
        plugin_name = self.get_plugin_name(extension)
        print(f"[DEBUG] Found file extension: '{extension}', Plugin name: '{plugin_name}'")

        # Add the plugin directory to sys.path
        sys.path.insert(0, self.directory)

        try:
            # Attempt to import the plugin module
            print(f"[DEBUG] Attempting to import plugin '{plugin_name}' and load the class...")
            plugin_module = importlib.import_module(plugin_name)
            class_name = extension.capitalize()  # Capitalize the class name to match convention
            plugin_class = getattr(plugin_module, class_name)
            
            # Create an instance of the plugin class and run the 'run' method for testing
            print(f"[DEBUG] Creating an instance of '{plugin_class.__name__}' for testing...")
            plugin_instance = plugin_class()
            
            print(f"[DEBUG] Running the 'run' method of '{plugin_class.__name__}' in test mode...")
            plugin_instance.run()  # In test mode, no file is passed
            print(f"[DEBUG] '{plugin_class.__name__}' successfully executed in test mode.")

        except (ModuleNotFoundError, AttributeError) as e:
            print(f"[ERROR] Error loading plugin '{plugin_name}': {e}")
        except Exception as e:
            print(f"[ERROR] Error running the plugin in test mode: {e}")
        finally:
            # Remove the plugin directory from sys.path after testing
            sys.path.pop(0)
