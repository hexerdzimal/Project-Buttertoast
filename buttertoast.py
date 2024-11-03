import sys
import argparse
from UI.gui_Loader import GUILoader
from UI.si_Loader import SILoader
from Engine.plugin_Loader import PluginLoader

image_path = "BuTo1.png"

def main():
    # Argumente parsen
    parser = argparse.ArgumentParser(description="Create a polyglot file by embedding a TrueCrypt or VeraCrypt volume into another file.")
    parser.add_argument('-gui', action='store_true', help="Launch the graphical user interface.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode for detailed output.")
    parser.add_argument('--testFile', help="Check a file by extension and run the corresponding plugin.")


    args = parser.parse_args()

    if args.gui:
        gui_loader = GUILoader(image_path)
        gui_loader.start_gui()
        return

    if args.testFile:
        # Lese die Datei ein, die geprüft werden soll
        try:
            with open(args.testFile, 'rb') as file:
                file_data = file.read()  # Lese den Inhalt der Datei
                print(f"[DEBUG] Datei '{args.testFile}' erfolgreich eingelesen. Größe: {len(file_data)} Bytes")
        except FileNotFoundError:
            print(f"[ERROR] Die Datei '{args.testFile}' wurde nicht gefunden.")
            sys.exit(1)

        # Erstelle eine Instanz des PluginLoaders und führe das Plugin aus
        plugin_loader = PluginLoader()
        plugin_loader.load_and_run_plugin(args.testFile, file_data)
        return

    else:
        shell_interface = SILoader()
        shell_interface.start_txt()

if __name__ == "__main__":
    
    main()

#a line