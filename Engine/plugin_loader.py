import importlib
import os
import sys
from Engine.plugin_Interface import PluginInterface  # Anpassung des Imports

class PluginLoader:
    def __init__(self, directory="plugins"):
        self.directory = directory

    def load_plugins(self):
        loaded_plugins = []
        
        # Prüfen, ob der plugins-Ordner existiert
        if not os.path.exists(self.directory):
            print(f"Plugin-Ordner '{self.directory}' nicht gefunden.")
            return loaded_plugins
        
        # Plugin-Ordner zum Python-Pfad hinzufügen
        sys.path.insert(0, self.directory)
        
        # Durchsuchen des Plugin-Ordners nach Python-Dateien
        for filename in os.listdir(self.directory):
            if filename.endswith(".py") and filename != "__init__.py":
                plugin_name = filename[:-3]
                try:
                    # Importiere das Plugin als Modul
                    plugin_module = importlib.import_module(plugin_name)
                    
                    # Suche nach Klassen, die das Plugin-Interface implementieren
                    for attribute_name in dir(plugin_module):
                        attribute = getattr(plugin_module, attribute_name)
                        if isinstance(attribute, type) and issubclass(attribute, PluginInterface) and attribute is not PluginInterface:
                            loaded_plugins.append(attribute())
                except Exception as e:
                    print(f"Fehler beim Laden des Plugins {plugin_name}: {e}")
        
        # Entferne den Plugin-Ordner
        sys.path.pop(0)
        
        return loaded_plugins