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


import importlib
import os
import sys

class PluginLoader:
    """
    A class responsible for loading and running plugins based on file extensions.
    It scans a specified directory for plugin files, loads them dynamically,
    and executes the plugin's main function.
    """

    def __init__(self, directory="buttertoast/plugins", ui=None):
        """
        Initializes the PluginLoader with a specified directory where the plugins are located
        and an optional UI to display messages.

        Args:
            directory (str): The directory to search for plugin files. Default is "plugins".
            ui (UI): Optional UI instance to display messages. If None, messages won't be displayed.
        """
        self.directory = directory  # Directory where plugins are located
        self.ui = ui  # UI instance for displaying messages
        
        # Debugging: print the current working directory and where we are looking for plugins
        current_dir = os.getcwd()
        plugin_path = os.path.join(current_dir, self.directory)
        
        if self.ui:
            self.ui.display_message(f"Current working directory: {current_dir}", "error")
            self.ui.display_message(f"Looking for plugins in: {plugin_path}", "error")

    def add_plugin_directory_to_sys_path(self):
        """
        Adds the plugin directory to sys.path to ensure that Python can locate plugins
        even if they are added dynamically or outside of the running environment.
        """
        if self.directory not in sys.path:
            sys.path.insert(0, self.directory)

    def remove_plugin_directory_from_sys_path(self):
        """
        Removes the plugin directory from sys.path after plugin execution to clean up.
        """
        if self.directory in sys.path:
            sys.path.remove(self.directory)

    def find_plugin_in_all_directories(self, extension):
        """
        Looks for a plugin in both the specified local plugin directory and global
        Python paths (including those installed via pip).

        Args:
            extension (str): The extension to find the plugin for.

        Returns:
            str: The name of the plugin module if found, or None.
        """
        # Try to find the plugin locally first
        plugin_name = self.get_plugin_name(extension)
        if plugin_name:
            return plugin_name
        
        # Try to find the plugin in globally installed packages
        self.add_plugin_directory_to_sys_path()
        plugin_name = self.get_plugin_name(extension)
        self.remove_plugin_directory_from_sys_path()
        
        return plugin_name

    def find_file_with_partition(self, extension):
        """
        Finds a file in the specified directory that starts with 'btp_' and ends with '.py'
        and contains the given extension in its partitioned filename.

        Args:
            extension (str): The string to search for in the partitioned filename.

        Returns:
            str: The filename of the matching file, or None if no match is found.
        """
        files = [f for f in os.listdir(self.directory) if f.startswith('btp_') and f.endswith('.py')]
        
        for file in files:
            partitions = file[4:-3].split('_')  # Remove "btp_" prefix and ".py" suffix
            
            if extension in partitions:
                return file
        
        if self.ui:
            self.ui.display_message(f"Could not find an extension for '{extension}'. Please check the plugin folder.", "error")
        return None

    def get_plugin_name(self, extension):
        """
        Generates the plugin name based on the file extension and searches for a plugin file 
        containing the given extension in its partitioned filename.

        Args:
            extension (str): The file extension (e.g., 'txt', 'json').

        Returns:
            str: The plugin name if the file is found, or None if no matching file is found.
        """
        found_file = self.find_file_with_partition(extension)
        
        if found_file:
            filename = found_file[:-3]  # Remove ".py" suffix
            return filename
        else:
            return None

    def load_and_run_plugin(self, volume_byte, host_byte, extension):
        """
        Loads and runs the plugin based on the file extension.

        Args:
            volume_byte (bytes): The bytecode data of the volume.
            host_byte (bytes): The bytecode data of the host.
            extension (str): The file extension.

        Returns:
            bytes: The processed bytecode after running the plugin.
        """
        if self.ui:
            self.ui.display_message(f"Trying to load the plugin for extension '{extension}'...", "verbose")
        
        plugin_name = self.find_plugin_in_all_directories(extension)
        if not plugin_name:
            return
        
        if self.ui:
            self.ui.display_message(f"Found file extension: '{extension}', Plugin name: '{plugin_name}'", "verbose")

        # Add the plugin directory to sys.path to locate the plugins
        self.add_plugin_directory_to_sys_path()

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
                self.ui.display_message(f"Error loading plugin '{plugin_name}': {e}", "error")
        except Exception as e:
            if self.ui:
                self.ui.display_message(f"Error executing the plugin: {e}", "error")
        finally:
            # Remove the plugin directory from sys.path after execution
            self.remove_plugin_directory_from_sys_path()

    def list_plugins(self):
        """
        Lists all available plugins in the specified directory, filtering for files that 
        follow the naming convention "btp_<extension>.py".

        Returns:
            list: A list of plugin names (without extensions) found in the directory.
        """
        available_plugins = []
        
        # Berechne den absoluten Pfad des Plugin-Ordners relativ zum Skript
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        plugin_path = os.path.join(project_root, self.directory)

        if not os.path.exists(plugin_path):
            if self.ui:
                self.ui.display_message(f"Plugin directory '{plugin_path}' not found.", "error")
            return available_plugins

        if self.ui:
            self.ui.display_message(f"Available plugins in the directory '{plugin_path}':", "info")
        
        for filename in os.listdir(plugin_path):
            if filename.startswith("btp_") and filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]  # Entferne die ".py"-Erweiterung
                try:
                    if self.ui:
                        self.ui.display_message(f"{plugin_name}", "info")
                except Exception as e:
                    if self.ui:
                        self.ui.display_message(f"Error loading plugin '{plugin_name}': {e}", "error")
        
        return available_plugins
