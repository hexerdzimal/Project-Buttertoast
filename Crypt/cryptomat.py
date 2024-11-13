# Autor: Fabian Kozlowski
# Der cryptomat dient der Ver- und Entschlüsselung während des Prozesses zur Erstellung einer polyglotten Datei
# Er unterstützt aktuell lediglich AES-XTS mit SHA512
# Anmerkung: Tatsächlich wird stets nur der Header ver- und entschlüsselt
# INPUT: Verschlüsseltes TrueCrypt-Volume (Binaerdaten / Bytecode), Passwort, Verschlüsseltes TrueCrypt-Polyglott (Binaerdaten / Bytecode)
# OUTPUT: "Neu"-Verschlüsseltes TrueCrypt-Volume (Binaerdaten / Bytecode)

import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# AES-XTS Konfiguration
AES_KEY_SIZE = 64
SALT_SIZE = 64
FULL_HEADER_SIZE = 512  # Header-Size eines TrueCrypt-Volumes inklusive SALT_SIZE
REAL_HEADER_SIZE = FULL_HEADER_SIZE - SALT_SIZE  # 448 bytes
TWEAK = b"\x00" * 16  # Der TWEAK bei AES-XTS besteht aus 16 Bytes, der Einfachheithalber als Nullen deklariert, kann auch random sein

class Cryptomat:
    def __init__(self):
        pass

    # Methode koordiniert die Entschlüsselung und Neu-Verschlüsselung. Sie entschlüsselt ein gegebenes TrueCrypt-Volume @encrypted_volume_1 und
    # versichert, dass dieser entschlüsselte Header (448 bytes ohne SALT) zum neuen Header von encrypted_volume_2 wird, welches
    # dann mit dem SALT von encrypted_volume_2 wieder verschlüsselt wird und zurückgegeben wird.
    # Input:
    #       @encrypted_volume, das unmodifizierte originale TrueCrypt-Volume
    #       @encrypted_polyglot, das modifizierte TrueCrypt-Volume welches den manipulierten SALT beinhaltet samt Host Datei
    #       @passphrase, das Passwort des TrueCrypt-Volumes
    # Output:
    #       @re_encrypted_volume_2, das modifizierte neu-verschlüsselte TrueCrypt-Volume
    def cryptomator(self, encrypted_volume: bytes, encrypted_polyglot: bytes, passphrase: str) -> bytes:
        # Entschlüsselung des TC-Volumes und der "polyglotten" Datei
        decrypted_volume = self.__decrypt_volume(encrypted_volume, passphrase)
        decrypted_polyglot = self.__decrypt_volume(encrypted_polyglot, passphrase)

        # Erstellung und Verschlüsselung der polyglotten Datei, dem Buttertoast
        decrypted_buttertoast = decrypted_polyglot[:64] + decrypted_volume[64:512] + decrypted_polyglot[512:]     # Die ersten 64 Byte kommen aus dem Polyglott, die nächsten 448 Bytes aus dem TC Volume (die Header-Daten), der Rest aus dem Polyglot
        encrypted_buttertoast = self.__encrypt_volume(decrypted_buttertoast, passphrase)

        #####
        return encrypted_buttertoast

    # Funktion zur Schlüsselableitung für AES
    def __derive_aes_keys(self, salt: bytes, passphrase: str) -> tuple:
        iterations = 1000
        hash_algo = hashes.SHA512()
        kdf = PBKDF2HMAC(
            algorithm=hash_algo,
            length=64,
            salt=salt,
            iterations=iterations,
        )
        key = kdf.derive(passphrase.encode())
        aes_key1 = key[:32]
        aes_key2 = key[32:]
        return aes_key1, aes_key2

    # Funktion zur Entschlüsselung eines verschlüsselten Volumens
    def __decrypt_volume(self, encrypted_volume: bytes, passphrase: str) -> bytes:
        # Extrahiere den Salt aus den ersten 64 Bytes des verschlüsselten Volumens
        salt = encrypted_volume[:64]

        # Erzeuge die AES-Schlüssel mit dem Salt und der Passphrase
        aes_key1, aes_key2 = self.__derive_aes_keys(salt, passphrase)

        # Initialisiere den AES-XTS Cipher zum Entschlüsseln
        cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(TWEAK))
        decryptor = cipher.decryptor()

        # Entschlüsseln des Volumens (ohne den Salt)
        decrypted_data = decryptor.update(encrypted_volume[64:]) + decryptor.finalize()

        # Überprüfung, ob die Entschlüsselung erfolgreich war und ein ASCII 'TRUE' erzeugt wurde
        if decrypted_data[:4] != b"TRUE":
            print("Fehler: Magic Number 'TRUE' nicht gefunden. Entschlüsselung fehlgeschlagen.")
            sys.exit(1)

        # Füge den Salt wieder hinzu und gebe die entschlüsselten Daten zurück
        return salt + decrypted_data

    # Funktion zur Verschlüsselung eines entschlüsselten Volumens
    def __encrypt_volume(self, decrypted_volume: bytes, passphrase: str) -> bytes:
        # Extrahiere den Salt aus den ersten 64 Bytes des entschlüsselten Volumens
        salt = decrypted_volume[:64]

        # Erzeuge die AES-Schlüssel mit dem Salt und der Passphrase
        aes_key1, aes_key2 = self.__derive_aes_keys(salt, passphrase)

        # Initialisiere den AES-XTS Cipher zum Verschlüsseln
        cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(TWEAK))
        encryptor = cipher.encryptor()

        # Verschlüssele das Volume (ohne den Salt)
        encrypted_data = encryptor.update(decrypted_volume[64:]) + encryptor.finalize()

        # Füge den Salt wieder hinzu und gebe die verschlüsselten Daten zurück
        return salt + encrypted_data






