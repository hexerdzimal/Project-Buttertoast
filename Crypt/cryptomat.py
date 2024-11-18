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
    #       @re_encrypted_buttertoast, das modifizierte neu-verschlüsselte TrueCrypt-Volume
    def cryptomator(self, encrypted_volume: bytes, encrypted_polyglot: bytes, passphrase: str) -> bytes:
        # Entschlüsselung des TC-Volumes
        decrypted_volume = self.__decrypt_volume(encrypted_volume, passphrase)

        # Neu-Verschlüsselung des TC-Volumes mit dem Daten aus dem verschlüsselten Polyglott (Host SALT)
        salt_poly = self.__salty(encrypted_polyglot) # 64 Bytes
        re_encrypted_volume = self.__encrypt_volume(salt_poly, decrypted_volume, passphrase)

        # Erstellung Buttertoast durch Kombination aus re_encrypted_volume und encrypted_polyglot
        # :512, darin sind der manipulierte SALT und der TrueCrypt-Header (neu verschlüsselt mit dem manipulierten SALT),
        # 512:, darin befindet sic - in genannter Reihenfolge - das TC-Volume (die eigentliche Daten) gefolgt von den Host-Daten
        encrypted_buttertoast = re_encrypted_volume[:512] + encrypted_polyglot[512:]

        return encrypted_buttertoast

    # Funktion gibt den SALT zurück
    def __salty(self, encrypted_volume) -> bytes:
        # -----------------------WORKAROUND---------------------------------------
        # WORKAROUND: Bei dem WAV (gefixed von Stefan) und TIFF skript liegt ein bytearray an! => Konvertierung!!!!
        if isinstance(encrypted_volume, bytearray):
            encrypted_volume = bytes(encrypted_volume)
        #---------------------------------------------------------------------------

        so_salty = encrypted_volume[:64]
        # Error handling für den Fall das so_salty nicht in bytes vorliegt
        if not isinstance(so_salty, bytes):
            raise ValueError("SALT muss vom Typ 'bytes' sein.")
        return so_salty

    # Funktion zur Schlüsselableitung für AES
    def __derive_aes_keys(self, salt: bytes, passphrase: str) -> tuple:
        # Error handling prüfe, ob der SALT tatsächlich in bytes vorliegt
        if not isinstance(salt, bytes):
            raise TypeError("SALT muss vom Typ 'bytes' sein um Schlüssel ableiten zu können.")

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

        # Entschlüsseln des Volumens (ohne Salt)
        decrypted_data = decryptor.update(encrypted_volume[64:]) + decryptor.finalize()

        # Überprüfung, ob die Entschlüsselung erfolgreich war und ein ASCII 'TRUE' erzeugt wurde
        if decrypted_data[:4] != b"TRUE":
            print("Fehler: Magic Number 'TRUE' nicht gefunden. Entschlüsselung fehlgeschlagen.")
            sys.exit(1)

        # Gebe die entschlüsselten Daten zurück
        return salt + decrypted_data

    # Funktion zur Verschlüsselung eines entschlüsselten Volumens
    def __encrypt_volume(self, salty: bytes, decrypted_volume: bytes, passphrase: str) -> bytes:
        # Extrahiere den Salt aus den ersten 64 Bytes des entschlüsselten Volumens
        #salt = decrypted_volume[:64]

        # Erzeuge die AES-Schlüssel mit dem Salt und der Passphrase
        aes_key1, aes_key2 = self.__derive_aes_keys(salty, passphrase)

        # Initialisiere den AES-XTS Cipher zum Verschlüsseln
        cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(TWEAK))
        encryptor = cipher.encryptor()

        # Verschlüssele das Volume (ohne Salt)
        encrypted_data = encryptor.update(decrypted_volume[64:]) + encryptor.finalize()

        # Gebe die verschlüsselten Daten zurück
        return salty + encrypted_data






