import os
from UI.BaseUI import BaseUI


class TUI(BaseUI):

    def open_file(self, file_type):
        """
        Öffnet eine Datei über die Eingabe eines Dateipfads und gibt den Pfad zurück.
        """
        while True:
            file_path = input(f"Bitte geben Sie den Pfad zur {file_type}-Datei ein: ")
            if os.path.exists(file_path):
                return file_path
            print(f"Die Datei {file_path} existiert nicht. Bitte versuchen Sie es erneut.")

    def save_file(self):
        """
        Lässt den Benutzer einen Speicherort auswählen und gibt den Pfad zurück.
        """
        return input("Bitte geben Sie den Pfad ein, an dem die Datei gespeichert werden soll: ")

    def enter_string(self, prompt):
        """
        Fordert den Benutzer auf, einen String einzugeben.
        """
        return input(f"{prompt}: ")

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

    def run(self):
        """
        Startet die TUI und bleibt aktiv.
        """
        while True:
            file1 = self.open_file("Eingabedatei 1")
            file2 = self.open_file("Eingabedatei 2")
            save_path = self.save_file()
            user_string = self.enter_string("Geben Sie einen beliebigen Text ein")

            if not file1 or not file2 or not save_path or not user_string:
                print("Fehler: Alle Eingaben müssen gemacht werden!")
                continue  # Wiederhole den Vorgang, anstatt die TUI zu schließen

            # Übergabe an den Controller
            self.controller.handle_user_input(file1, file2, user_string, save_path)

            # Optional: Exit-Mechanismus (falls gewünscht)
            exit_input = self.enter_string("Geben Sie 'exit' ein, um die Anwendung zu beenden")
            if exit_input.lower() == "exit":
                print("Beende die Anwendung.")
                break
