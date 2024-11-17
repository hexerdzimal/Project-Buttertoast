from tkinter import Tk, filedialog, simpledialog, messagebox
import tkinter as tk
import json
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
import os
from UI.BaseUI import BaseUI


class GUI(BaseUI):
    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.root.title("GUI")
        self.root.title("Buttertoast")
        self.root.geometry("500x500")
        self.root.minsize(500, 500)
        self.root.resizable(False, False)

        self.image_path = os.path.join(os.path.dirname(__file__), "..", "BuTo1.png")
        self.img = Image.open(self.image_path)
        self.img = self.img.resize((500, 500), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.img)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)
        self.bg_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        self.host_path = tk.StringVar()
        self.volume_path = tk.StringVar()
        self.save_path = tk.StringVar()
        self.password = tk.StringVar(value="buttertoast")
        self.show_password_var = tk.BooleanVar(value=False)

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_exit_click(None)) 
        self.root.mainloop()
    
    def create_widgets(self):
        self.password_entry = ttk.Entry(self.root, show="*", textvariable=self.password, width=10)
        self.show_password_checkbox = tk.Checkbutton(self.canvas, variable=self.show_password_var, command=self.toggle_password, bg="white")
        self.canvas.create_window(585, 10, anchor="nw", window=self.password_entry)
        self.canvas.create_window(660, 10, anchor="nw", window=self.show_password_checkbox)
        
        self.canvas.tag_bind(self.create_text_button("Host-Datei auswählen", 10, 10), "<Button-1>", self.on_host_click)
        self.canvas.tag_bind(self.create_text_button("Guest-Datei auswählen", 170, 10), "<Button-1>", self.on_volume_click)
        self.canvas.tag_bind(self.create_text_button("Speicherort auswählen", 340, 10), "<Button-1>", self.on_save_click)
        self.canvas.tag_bind(self.create_text_button("Ausführen", 100, 650, size=16), "<Button-1>", self.on_execute_click)
        self.canvas.tag_bind(self.create_text_button("Abbrechen", 500, 650, size=16), "<Button-1>", self.on_exit_click)

    def create_text_button(self, text, x, y, size=12):
        return self.canvas.create_text(x, y, text=text, font=("Helvetica", size), fill="black", activefill="yellow", anchor="nw")

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password_var.get() else "*")

    def on_host_click(self, event):
        self.host_path.set(self.openFile("Host"))

    def on_volume_click(self, event):
        self.volume_path.set(self.openFile("Guest"))

    def on_save_click(self, event):
        self.save_path.set(self.saveFile())

    def on_execute_click(self):
        # Die Ergebnisse werden hier zurückgegeben
        result = self.startProcessing(
            self.host_path.get(),
            self.volume_path.get(),
            self.password.get(),
            self.save_path.get()
        )
        # Resultate weitergeben
        print("Ergebnisse: ", result)
        return result

    def on_exit_click(self, event):
        if messagebox.askokcancel("Beenden", "Möchten Sie das Programm wirklich beenden?"):
            print("Das Programm wird beendet.")
            exit
            self.root.quit() 
        return None

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
            host = self.open_file("Host")
            guest = self.open_file("Guest")
            save_path = self.save_file()
            user_string = self.enter_string("Geben Sie einen beliebigen Text ein")

            if not host or not guest or not save_path or not user_string:
                messagebox.showerror("Fehler", "Alle Eingaben müssen gemacht werden!")
                continue  # Wiederhole den Vorgang, anstatt die GUI zu schließen

            # Übergabe an den Controller
            self.controller.handle_user_input(host, guest, user_string, save_path)
