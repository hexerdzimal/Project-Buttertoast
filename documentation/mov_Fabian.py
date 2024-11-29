import os
import struct
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# AES-XTS Konfiguration
AES_KEY_SIZE = 64  # AES-256 erfordert einen 64-Byte-Schlüssel im XTS-Modus
SALT_SIZE = 64  # Die ersten 64 Bytes sind der Salt
HEADER_SIZE = 512  # Gesamte TrueCrypt-Header-Größe
TWEAK = b"\x00" * 16  # Header-Tweak, null-initialisiert für TrueCrypt-Header

def open_file_dialog(prompt):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Dateiauswahl", prompt)
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path

# Funktion zum Speichern einer Datei mit einer Beschreibung
def save_file_dialog(prompt):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Speicherort auswählen", prompt)
    file_path = filedialog.asksaveasfilename(defaultextension=".bin")
    root.destroy()
    return file_path

def create_mov_skip_atom_salt(truecrypt_volume_size):
    atom_size = struct.pack('>I', truecrypt_volume_size)  # Dynamische Größe
    atom_type = b'skip'
    major_brand = b'isom'
    minor_version = b'\x00\x00\x00\x01'
    compatible_brands = b'isomiso2avc1mp41'[:12]
    skip_atom_salt = atom_size + atom_type + major_brand + minor_version + compatible_brands
    skip_atom_salt += b'\x00' * (SALT_SIZE - len(skip_atom_salt))  # Auffüllen auf 64 Bytes
    return skip_atom_salt

def derive_keys_with_pbkdf2(password, salt):
    key = PBKDF2(password, salt, dkLen=AES_KEY_SIZE, count=1000, prf=lambda p, s: HMAC.new(p, s, SHA512).digest())
    aes_key1 = key[:32]
    aes_key2 = key[32:]
    return aes_key1, aes_key2

def decrypt_header(salt, password, encrypted_header):
    aes_key1, aes_key2 = derive_keys_with_pbkdf2(password.encode(), salt)
    cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(TWEAK))
    decryptor = cipher.decryptor()
    decrypted_header = decryptor.update(encrypted_header) + decryptor.finalize()

    if decrypted_header[:4] != b"TRUE":
        print("Fehler: Magic Number 'TRUE' nicht gefunden. Entschlüsselung fehlgeschlagen.")
        sys.exit(1)

    return decrypted_header

def encrypt_header(salt, password, decrypted_header):
    aes_key1, aes_key2 = derive_keys_with_pbkdf2(password.encode(), salt)
    cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(TWEAK))
    encryptor = cipher.encryptor()
    encrypted_header = encryptor.update(decrypted_header) + encryptor.finalize()
    return encrypted_header

def create_modified_truecrypt_volume(original_file_path, new_header, output_path):
    shutil.copyfile(original_file_path, output_path)
    with open(output_path, "r+b") as modified_file:
        modified_file.seek(0)
        modified_file.write(new_header)
    print(f"Modifiziertes TrueCrypt-Volume mit neuem Header gespeichert unter {output_path}")

def append_complete_mov_as_atom(volume_path, mov_file_path):
    with open(mov_file_path, "rb") as mov_file:
        mov_data = mov_file.read()
    with open(volume_path, "ab") as volume_file:
        volume_file.write(mov_data)
    print(f"Komplette MOV-Datei erfolgreich als ATOM2 an {volume_path} angehängt.")

def adjust_stco_offsets(file_path, skip_atom_size):
    with open(file_path, "r+b") as f:
        data = f.read()
        stco_index = data.find(b'stco')
        if stco_index == -1:
            print("stco Atom nicht gefunden!")
            return

        offset_count_index = stco_index + 8
        offset_count = struct.unpack(">I", data[offset_count_index:offset_count_index + 4])[0]
        print(f"[DEBUG] Anzahl der Offsets im stco Atom: {offset_count}")
        offset_table_index = offset_count_index + 4

        for i in range(offset_count):
            current_offset_index = offset_table_index + (i * 4)
            current_offset = struct.unpack(">I", data[current_offset_index:current_offset_index + 4])[0]
            adjusted_offset = current_offset + skip_atom_size
            f.seek(current_offset_index)
            f.write(struct.pack(">I", adjusted_offset))

        print("Offsets im stco Atom erfolgreich angepasst.")

def main():
    original_file_path = open_file_dialog("Bitte wählen Sie die TrueCrypt-Volume-Datei zur Header-Extraktion aus")
    mov_file_path = open_file_dialog("Bitte wählen Sie die MOV-Datei zur Einbettung als ATOM aus")

    print("Extrahiere TrueCrypt-Header...")
    with open(original_file_path, "rb") as file:
        header = file.read(HEADER_SIZE)
    salt = header[:SALT_SIZE]
    encrypted_header = header[SALT_SIZE:]

    password = simpledialog.askstring("Passwort-Eingabe", "Geben Sie das Passwort für das TrueCrypt-Volume ein:")
    decrypted_header = decrypt_header(salt, password, encrypted_header)
    print("Header erfolgreich entschlüsselt.")

    truecrypt_volume_size = os.path.getsize(original_file_path)  # Dynamische Größe
    print(truecrypt_volume_size)
    new_salt = create_mov_skip_atom_salt(truecrypt_volume_size)
    encrypted_header_with_skip_atom_salt = encrypt_header(new_salt, password, decrypted_header)
    new_complete_header_skip_atom = new_salt + encrypted_header_with_skip_atom_salt

    output_path = save_file_dialog("Speichern des finalen MOV-Polyglot") + ".mov"
    create_modified_truecrypt_volume(original_file_path, new_complete_header_skip_atom, output_path)
    append_complete_mov_as_atom(output_path, mov_file_path)
    adjust_stco_offsets(output_path, truecrypt_volume_size)  # Dynamische Größe

if __name__ == "__main__":
    main()

#