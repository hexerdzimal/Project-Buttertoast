from UI.testMasterUI import BaseUI

class TUI(BaseUI):
    def __init__(self, event_manager):
        super().__init__(event_manager)

    def run(self):
        """
        Hauptmenü der TUI. Der Benutzer wählt, ob er zur Dateneingabe möchte
        oder eine andere Aktion ausführen will.
        """
        while True:
            print("\nWillkommen zur TUI!")
            print("1: Dateneingabe und Verarbeitung starten")
            print("2: Daten auflisten")
            print("3: Beenden")

            choice = input("Bitte wählen Sie eine Option: ").strip()

            if choice == "1":
                self.data_input_menu()
            elif choice == "2":
                self.trigger_list_data()
            elif choice == "3":
                print("Auf Wiedersehen!")
                break
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")

    def data_input_menu(self):
        """
        Führt den Benutzer durch die Dateneingabe und löst den 'process_data'-Event aus.
        """
        print("\n--- Dateneingabe ---")
        host = input("Host-Datei Pfad: ").strip()
        volume = input("Volume-Datei Pfad: ").strip()
        password = input("Passwort: ").strip()
        output = input("Ausgabedatei Pfad: ").strip()

        print("Tippen Sie 'start', um zu beginnen.")
        command = input("> ").strip().lower()
        if command == "start":
            self.event_manager.trigger_event("process_data", {
                "host": host,
                "volume": volume,
                "password": password,
                "output": output,
            })
        else:
            print("Abgebrochen.")

    def trigger_list_data(self):
        """
        Löst das Event 'list_data' aus.
        """
        print("\n--- Daten auflisten ---")
        self.event_manager.trigger_event("list_data", None)

    def show_result(self, result):
        """
        Zeigt das Ergebnis der Verarbeitung an.
        """
        print(f"Ergebnis: {result}")

    def show_error(self, message):
        """
        Zeigt eine Fehlermeldung an.
        """
        print(f"Fehler: {message}")
