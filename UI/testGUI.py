import tkinter as tk
from tkinter import messagebox
from UI.testMasterUI import BaseUI

import tkinter as tk

class GUI(BaseUI):
    def run(self):
        """
        Startet die GUI.
        """
        self.root = tk.Tk()
        self.root.title("GUI App")

        # Eingabefelder erstellen
        self.host_entry = self.create_input_field("Host-Datei Pfad")
        self.volume_entry = self.create_input_field("Volume-Datei Pfad")
        self.password_entry = self.create_input_field("Passwort")
        self.output_entry = self.create_input_field("Ausgabedatei Pfad")

        # Button hinzufügen
        process_button = tk.Button(self.root, text="Verarbeiten", command=self.on_process_button_click)
        process_button.pack(pady=10)

        self.root.mainloop()

    def create_input_field(self, label_text):
        """
        Hilfsfunktion, um ein Eingabefeld mit einem Label zu erstellen.
        """
        label = tk.Label(self.root, text=label_text)
        label.pack(pady=5)
        entry = tk.Entry(self.root)
        entry.pack(pady=5)
        return entry

    def on_process_button_click(self):
        """
        Button-Handler, der das 'process_data'-Event auslöst.
        """
        data = {
            "host": self.host_entry.get(),
            "volume": self.volume_entry.get(),
            "password": self.password_entry.get(),
            "output": self.output_entry.get()
        }
        self.event_manager.trigger_event("process_data", data)

    def show_result(self, result):
        """
        Zeigt das Ergebnis in einem Dialogfenster an.
        """
        status = result.get("status", "Unbekannter Status")
        message = f"Status: {status}"
        if "error_message" in result:
            message += f"\nFehler: {result['error_message']}"
        
        tk.messagebox.showinfo("Ergebnis", message)

    def show_error(self, message):
        """
        Zeigt eine Fehlermeldung in einem Dialogfenster an.
        """
        tk.messagebox.showerror("Fehler", message)

    def edit_config():
        """
        Menü zum Bearbeiten der Einstellungen in der Config

        """
