# Autor: Fabian Kozlowski
# Der cryptomat dient der Ver- und Entschlüsselung während des Prozesses zur Erstellung einer polyglotten Datei
# Er unterstützt aktuell lediglich AES-XTS mit SHA512
# INPUT: Verschlüsseltes TrueCrypt-Volume (Binaerdaten / Bytecode), Passwort, Verschlüsseltes TrueCrypt-Polyglott (Binaerdaten / Bytecode)
# OUTPUT: "Neu"-Verschlüsseltes TrueCrypt-Volume (Binaerdaten / Bytecode)

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512, HMAC
import binascii
import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class Cryptomat:

    # AES-XTS Konfiguration
    AES_KEY_SIZE = 64
    SALT_SIZE = 64
    FULL_HEADER_SIZE = 512 # Header-Size eines TrueCrypt-Volumes inklusive SALT_SIZE
    REAL_HEADER_SIZE = FULL_HEADER_SIZE - SALT_SIZE # 448 bytes
    TWEAK = b"\x00" * 16 # Der TWEAK bei AES-XTS besteht aus 16 Bytes, der Einfachheithalber als Nullen deklariert, kann auch random sein

    # Methode koordiniert die Entschlüsselung und Neu-Verschlüsselung. Sie entschlüsselt ein gegebenes TrueCrypt-Volume @encrypted_volume_1 und
    # versichert, dass dieser entschlüsselte Header (448 bytes ohne SALT) zum neuen Header von encrypted_volume_2 wird, welches
    # dann mit dem SALT von encrypted_volume_2 wieder verschlüsselt wird und zurückgegeben wird.
    # Input:
    #       @encrypted_volume_1, das unmodifizierte originale TrueCrypt-Volume
    #       @encrypted_volume_2, das modifizierte TrueCrypt-Volume welches den manipulierten SALT beinhaltet
    #       @password, das Passwort des TrueCrypt-Volumes
    # Output:
    #       @re_encrypted_volume_2, das modifizierte neu-verschlüsselte TrueCrypt-Volume
    def cryptomator(self, encrypted_volume_1: bytes, encrypted_volume_2: bytes, password: str) -> bytes:
        self.password = password



