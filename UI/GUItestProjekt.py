import tkinter as tk
import os
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# Funktionen
def choose_host():
    host_path.set(filedialog.askopenfilename(title="Host Datei auswählen"))

def choose_guest():
    guest_path.set(filedialog.askopenfilename(title="Guest-Datei auswählen"))

# Hier muss die Verschmelzung ausgeführt werden
def choose_exe():
    pass

def choose_cancel():
    root.quit()

def choose_save_location():
    file = filedialog.asksaveasfilename(title="Speicherort für entschlüsselte Datei auswählen")
    save_path.set(file)

def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# GUI einrichten
root = tk.Tk()
root.title("Buttertoast")
root.geometry("700x700")
root.minsize(700, 700)  # Größe setzen
root.resizable(False, False)  # Fenstergröße nicht veränderbar

# Hintergrundbild laden
image_path = os.path.join(os.path.dirname(__file__), "..", "BuTo1.png")
img = Image.open(image_path)
img = img.resize((700, 700), Image.LANCZOS)
background_image = ImageTk.PhotoImage(img)

# Canvas erstellen
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)
bg_image_id = canvas.create_image(0, 0, anchor="nw", image=background_image)

# GUI-Elemente hinzufügen
host_path = tk.StringVar()
guest_path = tk.StringVar()
save_path = tk.StringVar()

password_entry = ttk.Entry(root, show="*", width=10)
password_entry.insert(0, "buttertoast")
show_password_var = tk.BooleanVar(value=False)
show_password_checkbox = tk.Checkbutton(canvas, variable=show_password_var, command=toggle_password, bg="white")

# Save Button 
save_button = ttk.Button(canvas, text="Speicherort für das Polyglott auswählen", command=choose_save_location)
save_label = tk.Label(canvas, textvariable=save_path, fg="blue", bg="white")

# Text-Buttons auf Canvas
hostButtonNeu = canvas.create_text(10, 10, text="Host-Datei auswählen", font=("Helvetica", 12), fill="black", activefill="yellow", anchor="nw")
guestButtonNeu = canvas.create_text(170, 10, text="Guest-Datei auswählen", font=("Helvetica", 12), fill="black", activefill="yellow", anchor="nw")
saveButtonNeu = canvas.create_text(340, 10, text="Speicherort auswählen", font=("Helvetica", 12), fill="black", activefill="yellow", anchor="nw")
passworTextNeu = canvas.create_text(510, 10, text="Passwort:", font=("Helvetica", 12), fill="black", activefill="yellow", anchor="nw")

executeButtonNeu = canvas.create_text(100, 650, text="Ausführen", font=("Helvetica", 16), fill="black", activefill="yellow", anchor="nw")
cancelButtonNeu = canvas.create_text(500, 650, text="Abbrechen", font=("Helvetica", 16), fill="black", activefill="yellow", anchor="nw")

canvas.create_window(585, 10, anchor="nw", window=password_entry)
canvas.create_window(660, 10, anchor="nw", window=show_password_checkbox)

# Event-Handler
def on_host_button_click(event):
    choose_host()

def on_guest_button_click(event):
    choose_guest()

def on_exe_button_click(event):
    choose_exe()

def on_cancel_button_click(event):
    choose_cancel()

def on_save_button_click(event):
    choose_save_location()

canvas.tag_bind(hostButtonNeu, "<Button-1>", on_host_button_click)
canvas.tag_bind(guestButtonNeu, "<Button-1>", on_guest_button_click)
canvas.tag_bind(saveButtonNeu, "<Button-1>", on_save_button_click)
canvas.tag_bind(executeButtonNeu, "<Button-1>", on_exe_button_click)
canvas.tag_bind(cancelButtonNeu, "<Button-1>", on_cancel_button_click)

root.mainloop()
