import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptomat import Cryptomat

def select_file(prompt):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Dateiauswahl", prompt)
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def save_file_dialog(prompt):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Speicherort auswählen", prompt)
    file_path = filedialog.asksaveasfilename(defaultextension=".bin")
    root.destroy()
    return file_path

def load_binary_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()

def save_binary_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(data)

def main():
    # Nutzer nach dem TrueCrypt-Volume fragen
    tc_volume_path = select_file("Bitte wählen Sie das verschlüsselte TrueCrypt-Volume aus.")
    if not tc_volume_path:
        print("TrueCrypt-Volume nicht ausgewählt. Abbruch.")
        return
    tc_volume_data = load_binary_file(tc_volume_path)

    # Passwort für das TrueCrypt-Volume abfragen
    root = tk.Tk()
    root.withdraw()
    password = simpledialog.askstring("Passwort eingeben", "Geben Sie das Passwort für das TrueCrypt-Volume ein:", show='*')
    root.destroy()
    if not password:
        print("Passwort nicht eingegeben. Abbruch.")
        return

    # Nutzer nach dem verschlüsselten Polyglot fragen
    polyglot_path = select_file("Bitte wählen Sie das verschlüsselte Polyglot-Volume aus.")
    if not polyglot_path:
        print("Polyglot-Datei nicht ausgewählt. Abbruch.")
        return
    polyglot_data = load_binary_file(polyglot_path)

    # Speicherort für die Ausgabedatei wählen
    output_path = save_file_dialog("Speicherort für die Ausgabe-Datei auswählen")
    if not output_path:
        print("Kein Speicherort für die Ausgabe-Datei ausgewählt. Abbruch.")
        return

    # Cryptomat verwenden
    cryptomat = Cryptomat()
    try:
        result = cryptomat.cryptomator(tc_volume_data, polyglot_data, password)
        save_binary_file(output_path, result)
        print(f"Die Datei wurde erfolgreich neu verschlüsselt und unter {output_path} gespeichert.")
    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")

if __name__ == "__main__":
    main()
