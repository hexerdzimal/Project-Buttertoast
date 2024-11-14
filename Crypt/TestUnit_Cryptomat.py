import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptomat import Cryptomat
from plugins.Test_btp_png import Png  # Importing Png class
from plugins.Test_btp_wav import Wav  # Importing Wav class

# Kommentar 14.11: PNG funktioniert! WAV funktioniert nicht!

def select_file(prompt):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Dateiauswahl", prompt)
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

def save_file_dialog(prompt, default_extension=".bin"):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Speicherort auswählen", prompt)
    file_path = filedialog.asksaveasfilename(defaultextension=default_extension)
    root.destroy()
    return file_path

def load_binary_file(file_path):
    with open(file_path, "rb") as file:
        return file.read()

def save_binary_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(data)

def main():
    # Prompt user to select the encrypted TrueCrypt volume
    tc_volume_path = select_file("Bitte wählen Sie das verschlüsselte TrueCrypt-Volume aus.")
    if not tc_volume_path:
        print("TrueCrypt-Volume nicht ausgewählt. Abbruch.")
        return

    tc_volume_data = load_binary_file(tc_volume_path)

    # Ask for the password for the TrueCrypt volume
    root = tk.Tk()
    root.withdraw()
    password = simpledialog.askstring("Passwort eingeben", "Geben Sie das Passwort für das TrueCrypt-Volume ein:")
    root.destroy()
    if not password:
        print("Passwort nicht eingegeben. Abbruch.")
        return

    # Ask the user to choose between PNG and WAV polyglot creation
    root = tk.Tk()
    root.withdraw()
    file_type = simpledialog.askstring("Dateityp auswählen", "Geben Sie den Dateityp für die Polyglot-Erstellung ein (png/wav):")
    root.destroy()

    if file_type.lower() == "png":
        # PNG polyglot creation
        host_path = select_file("Bitte wählen Sie die PNG-Host-Datei für die Polyglot-Erstellung aus.")
        if not host_path:
            print("PNG-Host-Datei nicht ausgewählt. Abbruch.")
            return
        host_data = load_binary_file(host_path)

        # Set output file extension to .png
        polyglot_output_path = save_file_dialog("Speicherort für die Polyglot-Datei auswählen", default_extension=".png")
        if not polyglot_output_path:
            print("Kein Speicherort für die Polyglot-Datei ausgewählt. Abbruch.")
            return

        # Create polyglot content using the Png plugin
        png_plugin = Png()
        polyglot_data = png_plugin.run(tc_volume_data, host_data)

    elif file_type.lower() == "wav":
        # WAV polyglot creation
        host_path = select_file("Bitte wählen Sie die WAV-Host-Datei für die Polyglot-Erstellung aus.")
        if not host_path:
            print("WAV-Host-Datei nicht ausgewählt. Abbruch.")
            return
        host_data = load_binary_file(host_path)

        # Set output file extension to .wav
        polyglot_output_path = save_file_dialog("Speicherort für die Polyglot-Datei auswählen", default_extension=".wav")
        if not polyglot_output_path:
            print("Kein Speicherort für die Polyglot-Datei ausgewählt. Abbruch.")
            return

        # Create polyglot content using the Wav plugin
        wav_plugin = Wav()
        polyglot_data = wav_plugin.run(tc_volume_data, host_data)

    else:
        print("Ungültiger Dateityp. Abbruch.")
        return

    # Save the polyglot file
    save_binary_file(polyglot_output_path, polyglot_data)
    print(f"Polyglot-Datei wurde erfolgreich unter {polyglot_output_path} gespeichert.")

    # Prompt user to select the save location for the final encrypted output file
    output_path = save_file_dialog("Speicherort für die endgültige Ausgabe-Datei auswählen", default_extension=".bin")
    if not output_path:
        print("Kein Speicherort für die endgültige Ausgabe-Datei ausgewählt. Abbruch.")
        return

    # Use Cryptomat to encrypt the modified TrueCrypt volume with polyglot
    cryptomat = Cryptomat()
    try:
        result = cryptomat.cryptomator(tc_volume_data, polyglot_data, password)
        save_binary_file(output_path, result)
        print(f"Die endgültige Datei wurde erfolgreich neu verschlüsselt und unter {output_path} gespeichert.")
    except Exception as e:
        print(f"Fehler bei der Verarbeitung: {e}")

if __name__ == "__main__":
    main()
