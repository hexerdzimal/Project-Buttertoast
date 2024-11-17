import sys
import os
import json
import argparse
from Engine.engine import Engine



def load_config(config_file='config.json'):
    """
    Lädt die Konfiguration aus der angegebenen JSON-Datei im Verzeichnis der Hauptdatei.
    Erstellt eine Standard-Konfigurationsdatei, falls keine gefunden wird.
    """
    # Verzeichnis der aktuellen Datei (wo die main-Methode liegt)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)

    default_config = {
        "gui": True,
        "verbose": False
    }

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"[WARNUNG] Die Konfigurationsdatei '{config_path}' wurde nicht gefunden. Es wird eine Standarddatei erstellt.")
        save_config(default_config, config_path)
        return default_config
    except json.JSONDecodeError:
        print("[ERROR] Fehler beim Laden der JSON-Konfigurationsdatei.")
        sys.exit(1)


def save_config(config, config_file='config.json'):
    """
    Speichert die geänderte Konfiguration in der JSON-Datei im Verzeichnis der Hauptdatei.
    """
    # Verzeichnis der aktuellen Datei (wo die main-Methode liegt)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)

    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"[INFO] Konfiguration erfolgreich gespeichert in '{config_path}'.")
    except Exception as e:
        print(f"[ERROR] Fehler beim Speichern der Konfigurationsdatei: {e}")
        sys.exit(1)



def parse_arguments():
    
    # Parst die Kommandozeilenargumente und gibt ein Namespace-Objekt mit den Werten zurück.
    
    parser = argparse.ArgumentParser(description="Create a polyglot file by embedding a TrueCrypt or VeraCrypt volume into another file.")

    parser.add_argument('--testFile', help="Check a file by extension and run the corresponding plugin.")
    parser.add_argument('--changeui', '-cui', action='store_true', help="Toggle the GUI setting in the configuration.")
    parser.add_argument('--changeverbose', '-cv', action='store_true', help="Toggle the verbose setting in the configuration.")

    return parser.parse_args()




def main():
    # Konfiguration laden
    config = load_config()

    # Argumente parsen
    args = parse_arguments()

    # Flag, um zu überprüfen, ob Änderungen an der Konfiguration vorgenommen wurden
    config_changed = False

    # Konfiguration basierend auf den Argumenten aktualisieren
    if args.changeui:
        # Toggle the 'gui' setting
        new_gui_value = not config.get('gui', False)  # Wenn 'gui' nicht existiert, wird False als Default verwendet.
        if config['gui'] != new_gui_value:  # Nur speichern, wenn sich der Wert geändert hat
            config['gui'] = new_gui_value
            config_changed = True

    if args.changeverbose:
        # Toggle the 'verbose' setting
        new_verbose_value = not config.get('verbose', False)  # Wenn 'verbose' nicht existiert, wird False als Default verwendet.
        if config['verbose'] != new_verbose_value:  # Nur speichern, wenn sich der Wert geändert hat
            config['verbose'] = new_verbose_value
            config_changed = True

    # Speichern der geänderten Konfiguration nur, wenn sie geändert wurde
    if config_changed:
        save_config(config)

    # Wenn eine Datei zum Testen angegeben wurde
    if args.testFile:
        try:
            with open(args.testFile, 'rb') as file:
                file_data = file.read()  # Lese den Inhalt der Datei
                print(f"[DEBUG] Datei '{args.testFile}' erfolgreich eingelesen. Größe: {len(file_data)} Bytes")
        except FileNotFoundError:
            print(f"[ERROR] Die Datei '{args.testFile}' wurde nicht gefunden.")
            sys.exit(1)

        # Erstelle eine Instanz des PluginLoaders und führe das Plugin aus
        engine = Engine()
        engine.testFile()
        return

    # Hauptprogramm starten, wenn keine keine Testdatei angegeben ist
    
    engine = Engine()
    engine.start()



if __name__ == "__main__":
    main()