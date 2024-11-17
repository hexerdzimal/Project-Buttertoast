from tkinter import Tk, filedialog, simpledialog, messagebox
from UI.BaseUI import BaseUI


class GUI(BaseUI):
    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.root.title("GUI")

    def open_file(self, file_type):
        """
        Öffnet eine Datei über einen Dialog.
        """
        return filedialog.askopenfilename(title=f"Wählen Sie die {file_type}-Datei aus")

    def save_file(self):
        """
        Lässt den Benutzer einen Speicherort auswählen.
        """
        return filedialog.asksaveasfilename(title="Speicherort auswählen")

    def enter_string(self, prompt):
        """
        Fordert den Benutzer auf, einen String einzugeben.
        """
        return simpledialog.askstring("Eingabe", prompt)

    def show_result(self, result):
        """
        Zeigt das Ergebnis der Verarbeitung an.
        """
        messagebox.showinfo("Ergebnis", result)

    def show_error(self, message):
        """
        Zeigt eine Fehlermeldung an.
        """
        messagebox.showerror("Fehler", message)

    def run(self):
        """
        Startet die GUI und bleibt aktiv.
        """
        while True:
            file1 = self.open_file("Eingabedatei 1")
            file2 = self.open_file("Eingabedatei 2")
            save_path = self.save_file()
            user_string = self.enter_string("Geben Sie einen beliebigen Text ein")

            if not file1 or not file2 or not save_path or not user_string:
                messagebox.showerror("Fehler", "Alle Eingaben müssen gemacht werden!")
                continue  # Wiederhole den Vorgang, anstatt die GUI zu schließen

            # Übergabe an den Controller
            self.controller.handle_user_input(file1, file2, user_string, save_path)

            # Optional: Exit-Mechanismus (falls gewünscht)
            exit_input = self.enter_string("Geben Sie 'exit' ein, um die Anwendung zu beenden")
            if exit_input.lower() == "exit":
                self.root.quit()  # Beendet die GUI
                break

