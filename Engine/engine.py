import os
import json
from Engine.plugin_Loader import PluginLoader
from UI.BaseUI import BaseUI
from UI.tui import TUI  
from UI.gui import GUI        
from tkinter import messagebox

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


    def process_data(self, host, volume, password, output):
        """Verarbeitet die Daten."""
        print(f"Verarbeite Daten: Host={host}, Volume={volume}, Passwort={password}, Ausgabe={output}")

        return (host, volume, password, output)
    

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


    def handle_user_input(self, host, volume, password, output):
        """Methode, die von der UI aufgerufen wird, um Benutzereingaben zu verarbeiten."""
        try:
            # Eingaben validieren
            if not host or not volume or not password or not output:
                raise ValueError("Alle Eingaben müssen ausgefüllt sein!")

            # Daten verarbeiten
            result = self.process_data(host, volume, password, output)

            # Ergebnisse an die UI zurückgeben
            self.ui.show_result(result)
        except Exception as e:
            self.ui.show_error(f"Fehler bei der Verarbeitung: {str(e)}")
