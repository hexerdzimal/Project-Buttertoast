import importlib
import os
import sys


class PluginLoader:
    def __init__(self, directory="plugins"):
        # Verzeichnis, in dem sich die Plugins befinden
        self.directory = directory  
    
    def get_extension(self, filename):
        # Extrahiert die Dateiendung
        _, extension = os.path.splitext(filename)
        return extension[1:]  # Entfernt den Punkt
    
    def get_plugin_name(self, extension):
        # Erstellt den Plugin-Namen basierend auf der Dateiendung
        return f"btp_{extension}"
    
    def load_plugin(self, plugin_name, extension):
        # Lädt das Plugin-Modul und die zugehörige Klasse basierend auf der Dateiendung
        try:
            print(f"[DEBUG] Versuche, das Plugin '{plugin_name}' zu importieren und die Klasse zu laden...")
            plugin_module = importlib.import_module(plugin_name)
            class_name = extension.capitalize()
            return getattr(plugin_module, class_name)
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"[ERROR] Fehler beim Laden des Plugins '{plugin_name}': {e}")
            return None

    def run_plugin(self, plugin_class, file_data):
        # Erstellt eine Instanz der Plugin-Klasse und führt die 'run'-Methode aus
        try:
            print(f"[DEBUG] Erstelle eine Instanz von '{plugin_class.__name__}'...")
            plugin_instance = plugin_class()
            print(f"[DEBUG] Führe die run-Methode von '{plugin_class.__name__}' aus...")
            plugin_instance.run(file_data)                                                                       #<<<<<<<<<<<< HIER MUSS SPÄTER DER BIN CODE DER DATEIEN (CryptVol und Host) ÜBERGEBEN WERDEN
            print(f"[DEBUG] '{plugin_class.__name__}' erfolgreich ausgeführt.")
        except Exception as e:
            print(f"[ERROR] Fehler beim Ausführen des Plugins: {e}")

    def load_and_run_plugin(self, filename, file_data):
        # Hauptmethode zum Laden und Ausführen eines Plugins basierend auf dem Dateityp
        print(f"[DEBUG] Versuche, das Plugin für die Datei '{filename}' zu laden.")
        
        # Hole die Dateiendung und Plugin-Name
        extension = self.get_extension(filename)
        plugin_name = self.get_plugin_name(extension)
        print(f"[DEBUG] Gefundene Dateiendung: '{extension}', Plugin-Name: '{plugin_name}'")
        
        # Füge das Plugin-Verzeichnis zu sys.path hinzu
        sys.path.insert(0, self.directory)
        
        try:
            # Plugin-Klasse laden
            plugin_class = self.load_plugin(plugin_name, extension)
            if not plugin_class:
                return

            # Plugin ausführen
            self.run_plugin(plugin_class, file_data)
            
        finally:
            # Entferne das Plugin-Verzeichnis aus sys.path
            sys.path.pop(0)