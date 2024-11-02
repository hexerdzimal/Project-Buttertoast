import sys
import argparse
from UI.gui_Loader import GUILoader
from UI.si_Loader import SILoader
from Engine.plugin_Loader import PluginLoader

def main():
    # Argumente parsen
    parser = argparse.ArgumentParser(description="Verstecke eine Datei in einem TrueCrypt oder VeraCrypt Volume.")
    parser.add_argument('--vol', required=False, help="Der Pfad zum TrueCrypt oder VeraCrypt Volume.")
    parser.add_argument('--fil', required=False, help="Der Pfad zur Datei, in der das Volume versteckt werden soll.")
    parser.add_argument('--out', required=False, help="Der Pfad zur Zieldatei, in die das versteckte Volume gespeichert wird.")
    parser.add_argument('-gui', action='store_true', help="Starte die grafische Benutzeroberfläche.")
    parser.add_argument('--auto', action='store_true', help="Starte im automatischen Modus.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Aktiviere den Verbose-Modus für detailliertere Ausgaben.")
    parser.add_argument('--testFile', help="Prüfe eine Datei auf ihre Endung und führe das entsprechende Plugin aus.")

    args = parser.parse_args()

    if args.gui:
        gui_loader = GUILoader()
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
        plugin_loader.load_and_run_plugin(args.testFile)
        return

    # Überprüfe, ob der automatische Modus aktiviert ist
    if args.auto:
        # Stelle sicher, dass alle erforderlichen Parameter übergeben werden
        if not args.vol or not args.fil or not args.out:
            print("Im automatischen Modus müssen die Parameter --vol, --fil und --out angegeben werden.")
            sys.exit(1)

        # Hier kannst du die Logik für das Verstecken des Volumes implementieren
        # Füge hier weitere verbose Ausgaben nach Bedarf hinzu

    else:
        shell_interface = SILoader()
        shell_interface.start_txt()

if __name__ == "__main__":
    main()
