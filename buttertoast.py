import sys
import os
import json
import argparse
from Engine.engine import Engine;
from Engine.eventManager import EventManager



def load_config(config_file='config.json'):
    """
    Loads the configuration from the specified JSON file in the directory of the main script.
    Creates a default configuration file if none is found.

    Args:
        config_file (str): Name of the configuration file (default: 'config.json').

    Returns:
        dict: The loaded configuration as a dictionary.
    """
    # Directory of the current file (where the main method is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)

    default_config = {
        "gui": True,
        "verbose": False,
        "language": "en"
    }

    try:
        # Attempt to open and load the configuration file
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        # If the file is not found, create a default one
        print(f"[WARNING] Configuration file '{config_path}' not found. A default file will be created.")
        save_config(default_config, config_path)
        return default_config
    except json.JSONDecodeError:
        # Exit if the file contains invalid JSON
        print("[ERROR] Error loading the JSON configuration file. If this error persists, delete the config file in the program directory .")
        sys.exit(1)


def save_config(config, config_file='config.json'):
    """
    Saves the updated configuration to a JSON file in the directory of the main script.

    Args:
        config (dict): The configuration dictionary to save.
        config_file (str): Name of the configuration file (default: 'config.json').
    """
    # Directory of the current file (where the main method is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_file)

    try:
        # Attempt to write the configuration to the file
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"[INFO] Configuration successfully saved to '{config_path}'.")
    except Exception as e:
        # Handle any exceptions during file writing
        print(f"[ERROR] Error saving the configuration file: {e}")
        sys.exit(1)


def parse_arguments():
    """
    Parses command-line arguments and returns a Namespace object with the values.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create a polyglot file by embedding a TrueCrypt or VeraCrypt volume into another file."
    )

    parser.add_argument('--testFile', help="Check a file by extension and run the corresponding plugin.")
    parser.add_argument('--changeui', '-cui', action='store_true', help="Toggle the GUI setting in the configuration.")
    parser.add_argument('--changeverbose', '-cv', action='store_true', help="Toggle the verbose setting in the configuration.")

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

    # Flag to check if any changes were made to the configuration
    config_changed = False

    # Update the configuration based on command-line arguments
    if args.changeui:
        # Toggle the 'gui' setting
        new_gui_value = not config.get('gui', False)  # Default to False if 'gui' is not present
        if config['gui'] != new_gui_value:  # Only save if the value has changed
            config['gui'] = new_gui_value
            config_changed = True

    if args.changeverbose:
        # Toggle the 'verbose' setting
        new_verbose_value = not config.get('verbose', False)  # Default to False if 'verbose' is not present
        if config['verbose'] != new_verbose_value:  # Only save if the value has changed
            config['verbose'] = new_verbose_value
            config_changed = True

    # Save the configuration only if changes were made
    if config_changed:
        save_config(config)

    # If a file is specified for testing
    if args.testFile:
        try:
            # Attempt to read the file
            with open(args.testFile, 'rb') as file:
                file_data = file.read()  # Read the file content
                print(f"[DEBUG] File '{args.testFile}' successfully read. Size: {len(file_data)} bytes")
        except FileNotFoundError:
            print(f"[ERROR] File '{args.testFile}' not found.")
            sys.exit(1)

        # Create an instance of the Engine and execute the plugin
        engine = Engine()
        engine.testFile()
        return

    # Start the main program if no test file is specified
    
    event_manager = EventManager()
    engine = Engine(event_manager)
    engine.start()


if __name__ == "__main__":
    main()
