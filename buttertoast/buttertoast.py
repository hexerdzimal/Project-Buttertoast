import sys
import os
import json
import argparse
from buttertoast.Engine.engine import Engine;
from buttertoast.Engine.eventManager import EventManager


# path of the config file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.json')

def load_config(config_file=CONFIG_PATH):
    """
    Loads the configuration from the specified JSON file in the directory of the main script.
    Creates a default configuration file if none is found.

    Args:
        config_file (str): Name of the configuration file (default: 'config.json').

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    default_config = {
        "gui": False,
        "verbose": False,
        "check": False,
    }

    try:
        # Attempt to open and load the configuration file
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        # If the file is not found, create a default one
        print(f"[WARNING] Configuration file '{config_file}' not found. A default file will be created.")
        save_config(default_config, config_file)
        return default_config
    except json.JSONDecodeError:
        # Exit if the file contains invalid JSON
        print("[ERROR] Error loading the JSON configuration file. If this error persists, delete the config file in the program directory .")
        sys.exit(1)

def save_config(config, config_file=CONFIG_PATH):
    """
    Speichert die Konfiguration in einer JSON-Datei.

    Args:
        config (dict): Die zu speichernde Konfiguration.
        config_file (str): Der Pfad zur Konfigurationsdatei (default: 'config.json').
    """
    try:
        # Sicherstellen, dass der Pfad existiert
        os.makedirs(os.path.dirname(config_file), exist_ok=True)

        # Konfiguration als JSON speichern
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)

        print(f"[INFO] Konfiguration erfolgreich in '{config_file}' gespeichert.")

    except Exception as e:
        print(f"[ERROR] Fehler beim Speichern der Konfiguration: {e}")

import argparse

def parse_arguments():
    """
    Parses command-line arguments and returns a Namespace object with the values.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create a polyglot file by embedding a TrueCrypt or VeraCrypt volume into another file."
    )

    # Option für den CLI-Modus
    parser.add_argument(
        '-cli', 
        action='store_true', 
        help="Run the tool in CLI mode"
    )

    # Option für den verbose-Modus
    parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help="Enable verbose output"
    )

    # Falls -cli angegeben ist, müssen diese Argumente übergeben werden
    parser.add_argument(
        'host', 
        type=str, 
        nargs='?', 
        help="Path to the host file"
    )
    parser.add_argument(
        'volume', 
        type=str, 
        nargs='?', 
        help="Path to the volume file"
    )
    parser.add_argument(
        'password', 
        type=str, 
        nargs='?', 
        help="Password for the volume"
    )
    parser.add_argument(
        'output', 
        type=str, 
        nargs='?', 
        help="Path to the output file"
    )

    return parser.parse_args()



def main():
    """
    Main entry point of the application. Manages configuration loading, argument parsing,
    and interaction with the Engine.
    """
    # Load the configuration
    config = load_config()

    # Parse command-line arguments
    args = parse_arguments()
    verbose = args.verbose

    if args.cli:
        # Wenn im CLI-Modus, müssen die erforderlichen Argumente vorhanden sein
        if not all([args.host, args.volume, args.password, args.output]):
            print("Error: Missing required arguments for CLI mode. Please provide host, volume, password, and output.")
            return

        # Erstelle das "data" Paket
        data = {
            "host": args.host,
            "volume": args.volume,
            "password": args.password,
            "output": args.output
        }

        # Instanziiere den EventManager und Engine und rufe on_process_data auf
        event_manager = EventManager()
        engine = Engine(event_manager)
        
        # Rufe die on_process_data Methode auf
        engine.process_data_cli(data, verbose)
    else:
        # Falls nicht im CLI-Modus, nur den EventManager und Engine starten
        event_manager = EventManager()
        engine = Engine(event_manager)
        engine.start()


if __name__ == "__main__":
    main()
