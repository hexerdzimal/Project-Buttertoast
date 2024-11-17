import os
import json
from Engine.plugin_Loader import PluginLoader
from UI.BaseUI import BaseUI
from UI.TUI import TUI  
from UI.gui import GUI     
from Crypt.cryptomat import Cryptomat   


class Engine:

    def __init__(self):
        self.config = self.load_config()
        self.ui = None


    def load_config(self):
        """Lädt die Konfigurationsdatei."""
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, "config.json")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Die Konfigurationsdatei {config_path} wurde nicht gefunden.")
        
        with open(config_path, "r") as file:
            config = json.load(file)
        
        return config
    
    
    def select_ui(self):
  
        use_gui = self.config.get("gui", False)  # Standardwert ist False (TextUI)
        
        if use_gui:
            self.ui = GUI()
        else:
            self.ui = TUI()


    def start_ui(self):
        """Startet die UI und verknüpft sie mit der Engine."""
        self.ui = BaseUI()
        self.ui.set_controller(self)  # Übergibt die Engine als Controller an die UI


    def process_data(self, host, host_bytecode, volume_bytecode, password, output):
        """Verarbeitet die Daten, führt das Plugin aus und gibt das Ergebnis zurück."""
        print(f"Verarbeite Daten: Passwort={password}, Ausgabe={output}")

        # Beispiel: Hier kannst du weitere Logik zur Verarbeitung der Daten hinzufügen
        # Das Plugin wird mit den Bytecode-Daten aufgerufen
        try:
            # Plugin aufrufen

            plugin = PluginLoader
            poly_bytecode = plugin.load_and_run_plugin(host, volume_bytecode, host_bytecode)

            # Crypter aufrufen
            cryptomat = Cryptomat
            buttertoast = cryptomat.cryptomator(volume_bytecode, poly_bytecode, password)

            self.save_bytecode_to_file(buttertoast, output)  # 'output' als Dateiname verwenden

            return {"Datei erfolgreich erstellt"}
        except Exception as e:
            print(f"[ERROR] Fehler bei der Plugin-Ausführung: {e}")
            return {"status": "Fehler", "error_message": str(e)}


    def handle_user_input(self, host, volume, password, output):
        """Methode, die von der UI aufgerufen wird, um Benutzereingaben zu verarbeiten."""
        try:
            # Eingaben validieren
            if not host or not volume or not password or not output:
                raise ValueError("Alle Eingaben müssen ausgefüllt sein!")

            # Daten als Bytecode einlesen
            host_bytecode = self.read_file_as_bytecode(host)
            volume_bytecode = self.read_file_as_bytecode(volume)

            # Die Bytecode-Daten an die Verarbeitungsmethode weitergeben
            result = self.process_data(host, host_bytecode, volume_bytecode, password, output)

            # Ergebnisse an die UI zurückgeben
            self.ui.show_result(result)

        except Exception as e:
            self.ui.show_error(f"Fehler bei der Verarbeitung: {str(e)}")


    def read_file_as_bytecode(self, file_path):
        """Liest eine Datei ein und gibt deren Inhalt als Bytecode zurück."""
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Fehler beim Einlesen der Datei '{file_path}': {e}")
        
    def save_bytecode_to_file(self, bytecode: bytes, filename: str):
        """Speichert den gegebenen Bytecode in eine Datei."""
        try:
            with open(filename, 'wb') as file:
                file.write(bytecode)
            print(f"[DEBUG] Bytecode erfolgreich in die Datei '{filename}' geschrieben.")
        except Exception as e:
            print(f"[ERROR] Fehler beim Speichern des Bytecodes in die Datei '{filename}': {e}")

    

    def start(self):
        """
        Startet die Engine und initialisiert die UI.
        """
        try:
            self.select_ui()
            self.ui.set_controller(self)  # Verknüpft die UI mit der Engine
            self.ui.run()
        except Exception as e:
            print(f"Fehler beim Starten der Engine: {e}")

