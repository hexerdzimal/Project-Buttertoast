import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Funktionen
def decrypt_data(volume, hash_algo, password, data):
    if volume == 0:
        iterations = 1000
    elif volume == 1:
        iterations = 500000
    else:
        raise ValueError("0 = TrueCrypt, 1 = VeraCrypt")

    salt = data[:64]
    match hash_algo:
        case 0:
            hash_algo = hashes.SHA512()
        case 1:
            hash_algo = hashes.SHA256()
        case 2:
            hash_algo = hashes.BLAKE2s()
        case _:
            raise ValueError("Unsupported hash algorithm")

    kdf = PBKDF2HMAC(
        algorithm=hash_algo,
        length=64,
        salt=salt,
        iterations=iterations,
    )
    key = kdf.derive(password.encode())
    aes_key1, aes_key2 = key[:32], key[32:]
    tweak = bytes.fromhex('00000000000000000000000000000000')
    cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(tweak))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(data[64:]) + decryptor.finalize()

    return decrypted_data

# Action zuweisung
def choose_host():
    host_path.set(filedialog.askopenfilename(title="Host Datei auswählen"))
def choose_guest():
    guest_path.set(filedialog.askopenfilename(title="Guest-Datei auswählen"))
def choose_exe():
    execute
def choose_cancel():
    root.quit()

def choose_save_location():
    file = filedialog.asksaveasfilename(title="Speicherort für entschlüsselte Datei auswählen")
    save_path.set(file)

def execute():
    volume = volume_num[volume_choice.get()]
    hash_algo = hash_num[hash_choice.get()]
    password = password_entry.get()
    encrypted_file = file_path.get()
    decrypted_file = save_path.get()

    if not encrypted_file:
        messagebox.showwarning("Warnung", "Bitte eine verschlüsselte Datei auswählen.")
        return
    if not decrypted_file:
        messagebox.showwarning("Warnung", "Bitte einen Speicherort für die entschlüsselte Datei angeben.")
        return

    with open(encrypted_file, "rb") as f:
        data = f.read()

    decrypted_data = decrypt_data(volume, hash_algo, password, data)

    with open(decrypted_file, "wb") as f:
        f.write(decrypted_data)

    messagebox.showinfo("Info", f"Die Datei wurde gespeichert:\n{decrypted_file}")

def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

# GUI einrichten
root = tk.Tk()
root.title("Entschlüsselungstool")
root.geometry("700x700")

# Hintergrundbild laden und skalieren
image_path = "C:/Users/malte/Desktop/Sicherheit/BuTo1.png"
img = Image.open(image_path)
img = img.resize((700, 700), Image.LANCZOS)
background_image = ImageTk.PhotoImage(img)

canvas = tk.Canvas(root, width=700, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=background_image)

# Stil für die buttergelben Buttons festlegen
style = ttk.Style(root)
style.theme_use("clam")
butter_yellow = "#FFFACD" 
style.configure("TButton", font=("Helvetica", 12), foreground="black", background=butter_yellow, padding=10)
style.map("TButton",
          background=[("active", "#FFD700")]) 

# GUI-Elemente hinzufügen
host_path = tk.StringVar()
guest_path = tk.StringVar()
save_path = tk.StringVar()
volume_num = {"TrueCrypt": 0, "VeraCrypt": 1} 
hash_num = {"SHA512": 0, "SHA256": 1, "BLAKE2s": 2} 

# Transparenten Text auf dem Canvas erstellen
canvas.create_text(10, 70, anchor="nw", text="Volume auswählen:", font=("Helvetica", 12), fill="black")
canvas.create_text(10, 120, anchor="nw", text="Hash-Algorithmus auswählen:", font=("Helvetica", 12), fill="black")
canvas.create_text(10, 170, anchor="nw", text="Passwort eingeben:", font=("Helvetica", 12), fill="black")

# GUI-Eingabeelemente
volume_choice = tk.StringVar(value="TrueCrypt")
volume_menu = ttk.OptionMenu(root, volume_choice, "VeraCrypt", "TrueCrypt")

hash_choice = tk.StringVar(value="SHA512")
hash_menu = ttk.OptionMenu(root, hash_choice, "SHA512", "SHA256", "BLAKE2s")

password_entry = ttk.Entry(root, show="*")
password_entry.insert(0, "buttertoast")
show_password_var = tk.BooleanVar(value=False)
show_password_checkbox = tk.Checkbutton(root, variable=show_password_var, command=toggle_password, background="white") 

# Save Button and Label
save_button = ttk.Button(root, text="Speicherort für das Polyglott auswählen", command=choose_save_location)
save_label = tk.Label(root, textvariable=save_path, fg="blue", bg="white")

execute_button = ttk.Button(root, text="Ausführen", command=execute)
cancel_button = ttk.Button(root, text="Abbrechen", command=root.quit)

# Text-Button für Host-Datei erstellen
hostButtonNeu = canvas.create_text(10, 10, text="Host-Datei auswählen", font=("Helvetica", 16), fill="black", activefill="yellow", anchor="nw")
guestButtonNeu = canvas.create_text(260, 10, text="Guest-Datei auswählen", font=("Helvetica", 16), fill="black", activefill="yellow", anchor="nw")
executeButtonNeu = canvas.create_text(300, 650, text="Ausführen", font=("Helvetica", 16), fill="black", activefill="yellow", anchor="nw")
cancelButtonNeu = canvas.create_text(500, 650, text="Abbrechen", font=("Helvetica", 16), fill="black", activefill="yellow", anchor="nw")

# Event-Handler für den Host-Button
def on_host_button_click(event):
    choose_host()
 
def on_guest_button_click(event):
    choose_guest()

def on_exe_button_click(event):
    choose_exe()

def on_cancel_button_click(event):
    choose_cancel()

# Binde den Klick-Event an den Text
canvas.tag_bind(hostButtonNeu, "<Button-1>", on_host_button_click)
canvas.tag_bind(guestButtonNeu, "<Button-1>", on_guest_button_click)
canvas.tag_bind(executeButtonNeu, "<Button-1>", on_exe_button_click)
canvas.tag_bind(cancelButtonNeu, "<Button-1>", on_cancel_button_click)

# Elements Placement 
canvas.create_window(10, 90, anchor="nw", window=volume_menu)
canvas.create_window(10, 140, anchor="nw", window=hash_menu)

# Positioning password field next to host and guest file buttons
canvas.create_window(10, 190, anchor="nw", window=password_entry)
canvas.create_window(150, 190, anchor="nw", window=show_password_checkbox)

root.mainloop()
