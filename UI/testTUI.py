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
            print (r"""

                        
                            
                    +===================================================================================================+
                    |                                                                         Version: 0.1 (burnt) 2024 |
                    |   ██████╗ ██╗   ██╗████████╗████████╗███████╗██████╗ ████████╗ ██████╗  █████╗ ███████╗████████╗  |
                    |   ██╔══██╗██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝  |
                    |   ██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝   ██║   ██║   ██║███████║███████╗   ██║     |
                    |   ██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗   ██║   ██║   ██║██╔══██║╚════██║   ██║     |
                    |   ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║███████║   ██║     |
                    |   ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝     |
                    |                                   The melting pot for polyglot.                                   |
                    +===================================================================================================+
                                                    by Fabian Kozlowski, Stefan Leippe, Malte Muthesius, Matthias Ferstl

                        """)   

            print("1: Dateneingabe und Verarbeitung starten")
            print("2: Plugins auflisten")
            print("3: Einstellungen")
            print("4: Beenden")

            choice = input("Bitte wählen Sie eine Option: ").strip()

            if choice == "1":
                self.data_input_menu()
            elif choice == "2":
                self.trigger_list_data()
            elif choice == "3":
                self.edit_config()
            elif choice == "4":
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

    def edit_config(self):
        """
        Änderung der Einstellungen in der config.json
        """
        print("1: UserInterface wechseln")
        print("2: Verbosemodus wechseln")
        print("3: Spracheinstellungen")
        print("4: Zurück ins Hauptmenü")

        choice = input("Bitte wählen Sie eine Option: ").strip()

        if choice == "1":
            # Hier sollte das Event ausgelöst werden, um die UI zu wechseln
            self.event_manager.trigger_event("change_ui", None)
        elif choice == "2":
            self.event_manager.trigger_event("change_verbose", None)
        elif choice == "3":
            # Hier kannst du weitere Aktionen hinzufügen
            print("Spracheneinstellungen sind noch nicht implementiert.")
        elif choice == "4":
            self.run()  # Zurück zum Hauptmenü
        else:
            print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")


    def trigger_change_language(self):
        """
        Löst das Event 'change_language' aus.
        """
        print("\n--- Daten auflisten ---")
        self.event_manager.trigger_event("change_language", None)

    def trigger_change_ui(self):
        """
        Löst das Event 'change_ui' aus.
        """
        print("\n--- Daten auflisten ---")
        self.event_manager.trigger_event("change_ui", None)

    def trigger_change_verbose(self):
        """
        Löst das Event 'change_verbose' aus.
        """
        print("\n--- Daten auflisten ---")
        self.event_manager.trigger_event("change_verbose", None)

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


