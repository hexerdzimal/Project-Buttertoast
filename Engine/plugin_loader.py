import importlib
import os
import sys
from Engine.plugin_Interface import plugin_Interface

class PluginLoader:
    def __init__(self, directory="plugins"):
        self.directory = directory

    def load_and_run_plugin(self, filename):
        print(f"[DEBUG] Versuche, das Plugin für die Datei '{filename}' zu laden.")

        # Hole die Dateiendung
        _, extension = os.path.splitext(filename)
        extension = extension[1:]  # Entferne den Punkt
        print(f"[DEBUG] Gefundene Dateiendung: '{extension}'")

        # Baue den Plugin-Namen
        plugin_name = f"btp_{extension}"
        print(f"[DEBUG] Plugin-Name: '{plugin_name}'")

        # Listet die Dateien im Plugin-Verzeichnis auf
        print(f"[DEBUG] Suche nach Plugins im Verzeichnis: '{self.directory}'")
        try:
            # Zeige alle Dateien im Plugin-Verzeichnis an
            files = os.listdir(self.directory)
            print(f"[DEBUG] Vorhandene Dateien im Plugin-Verzeichnis: {files}")
        except FileNotFoundError:
            print(f"[ERROR] Das Verzeichnis '{self.directory}' wurde nicht gefunden.")
            return

        # Füge das Plugin-Verzeichnis zu sys.path hinzu
        sys.path.insert(0, self.directory)

        try:
            # Versuche, das Plugin zu importieren
            print(f"[DEBUG] Versuche, das Plugin '{plugin_name}' zu importieren...")
            plugin_module = importlib.import_module(plugin_name)

            # Dynamisch die Klasse vom Plugin laden
            class_name = extension.capitalize()  # Nimmt die Dateiendung und macht sie zum Klassennamen
            plugin_class = getattr(plugin_module, class_name)  # hole die Klasse anhand des Namens

            # Erstelle eine Instanz des Plugins
            print(f"[DEBUG] Erstelle eine Instanz von '{class_name}'...")
            plugin_instance = plugin_class()  # Nimm die konkrete Plugin-Klasse

            # Führe die run-Methode des Plugins aus
            print(f"[DEBUG] Führe die run-Methode von '{class_name}' aus...")
            plugin_instance.run()  
            print(f"[DEBUG] '{class_name}' erfolgreich ausgeführt.")

        except ModuleNotFoundError:
            print(f"[ERROR] Plugin '{plugin_name}' nicht gefunden.")
        except Exception as e:
            print(f"[ERROR] Fehler beim Ausführen des Plugins: {e}")
        finally:
            # Entferne das Plugin-Verzeichnis wieder aus sys.path
            sys.path.pop(0)
