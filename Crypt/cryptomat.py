# Author: Fabian Kozlowski
# Date: November 22, 2024
# The Cryptomat is used for encryption and decryption during the process of creating a polyglot file.
# Currently, it only supports AES-XTS with SHA512.
# Note: Only the header is encrypted and decrypted.
# INPUT: Encrypted TrueCrypt volume (binary data/bytecode), password, encrypted TrueCrypt polyglot (binary data/bytecode)

# OUTPUT: Re-encrypted TrueCrypt volume (binary data/bytecode) or a String with an Error-Message if the password was wrong


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# AES-XTS configuration
AES_KEY_SIZE = 64
SALT_SIZE = 64
FULL_HEADER_SIZE = 512  # Header size of a TrueCrypt volume, including SALT_SIZE
REAL_HEADER_SIZE = FULL_HEADER_SIZE - SALT_SIZE  # 448 bytes
TWEAK = b"\x00" * 16  # The tweak for AES-XTS consists of 16 bytes, here set to zeros for simplicity, but can be randomized.

class Cryptomat:
    """
    A class used to encrypt and decrypt data during the creation of polyglot files.
    This class focuses on the header of TrueCrypt volumes and manipulates the encryption
    using a modified salt derived from the polyglot host file.

    Attributes:
    ----------
    ui : UI or None
        Optional UI instance to display messages. If None, no messages will be displayed.
    """

    def __init__(self, ui=None):
        """
        Initialize the Cryptomat class.

        Parameters:
        ----------

        ui : UI, not mandatory

            Optional UI instance to display verbose messages during processing.
            If None, no messages will be displayed.
        """
        self.ui = ui  # UI instance for displaying messages


    def cryptomator(self, encrypted_volume: bytes, encrypted_polyglot: bytes, passphrase: str) -> str | bytes:

        """
        Coordinates decryption and re-encryption of a TrueCrypt volume header.
        The method ensures that the decrypted header (448 bytes excluding the salt)
        from the original volume becomes the new header of the polyglot volume.
        It uses the manipulated salt from the polyglot file for encryption.

        Parameters:
        encrypted_volume (bytes): The original unmodified TrueCrypt volume.
        encrypted_polyglot (bytes): The modified TrueCrypt volume containing the manipulated salt and host file data.
        passphrase (str): The password for the TrueCrypt volume.

        Returns:
        str: The error message when the password was wrong.


        bytes: The re-encrypted TrueCrypt volume (binary data), which includes the manipulated salt.
        """
        # Extract the salt from the polyglot file
        self.ui.display_message(f"Extracting the SALT from the polyglot file...", "verbose")
        salt_poly = self.__salty(encrypted_polyglot)  # 64 bytes
        self.ui.display_message(f"SALT extracted.", "verbose")

        # Decrypt the TrueCrypt volume
        self.ui.display_message(f"Decrypting the given TrueCrypt-Volume...", "verbose")
        decrypted_volume = self.__decrypt_volume(encrypted_volume, passphrase)
        if decrypted_volume is None:  # Abbruch bei fehlgeschlagener Entschlüsselung
            self.ui.display_message(f"Decryption failed. Wrong password or invalid volume.", "info")
            return None

        self.ui.display_message(f"TrueCrypt-Volume decrypted.", "verbose")

        # Check if the decryption was a success, meaning we got a TRUE
        # If it was not, the cryptomator returns a String with the error msg that the password was wrong or the TrueCrypt Volume is invalid
        if isinstance(decrypted_volume, str):
            # Return that string as the final result (error message)
            return "Wrong password provided or invalid TrueCrypt-Volume!"

        # Re-encrypt the volume using the salt from the polyglot host file
        self.ui.display_message(f"Re-encrypting the given TrueCrypt-Volume...", "verbose")
        re_encrypted_volume = self.__encrypt_volume(salt_poly, decrypted_volume, passphrase)
        self.ui.display_message(f"TrueCrypt-Volume re-encrypted with the manipulated SALT.", "verbose")

        # Combine the re-encrypted header and the original data/host data to create the polyglot
        self.ui.display_message(f"Creating the buttertoast aka polyglot file...", "verbose")
        encrypted_buttertoast = re_encrypted_volume[:512] + encrypted_polyglot[512:]
        self.ui.display_message(f"Buttertoast aka polyglot file created.", "verbose")

        return encrypted_buttertoast

    def __salty(self, encrypted_volume) -> bytes:
        """
        Extracts the salt (first 64 bytes) from the provided encrypted volume.

        Parameters:
        encrypted_volume (bytes or bytearray): The encrypted volume data.

        Returns:
        bytes: The extracted salt.

        Raises:
        ValueError: If the extracted salt is not of type 'bytes'.
        """
        # Workaround: Convert bytearray to bytes for compatibility
        if isinstance(encrypted_volume, bytearray):
            encrypted_volume = bytes(encrypted_volume)

        # Extract the first 64 bytes as salt
        so_salty = encrypted_volume[:64]

        # Validate the salt type
        if not isinstance(so_salty, bytes):
            raise ValueError("SALT must be of type 'bytes'.")
        return so_salty

    def __derive_aes_keys(self, salt: bytes, passphrase: str) -> tuple:
        """
        Derives AES-XTS encryption keys using the provided salt and passphrase.

        Parameters:
        salt (bytes): The salt used for key derivation.
        passphrase (str): The passphrase used for encryption.

        Returns:
        tuple: A tuple containing two AES keys (32 bytes each).

        Raises:
        TypeError: If the provided salt is not of type 'bytes'.
        """
        if not isinstance(salt, bytes):
            raise TypeError("SALT must be of type 'bytes' for key derivation.")

        self.ui.display_message(f"Deriving AES-keys...", "verbose")
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
        self.ui.display_message(f"AES-keys derived.", "verbose")
        return aes_key1, aes_key2


    def __decrypt_volume(self, encrypted_volume: bytes, passphrase: str) -> str | bytes:

        """
        Decrypts the provided TrueCrypt volume using AES-XTS with the derived keys.

        Parameters:
        encrypted_volume (bytes): The encrypted TrueCrypt volume.
        passphrase (str): The passphrase for decryption.

        Returns:

        str: The error message if the password was wrong.
        bytes: The decrypted volume, including the salt.

        """
        # Extract the salt from the first 64 bytes
        salt = encrypted_volume[:64]

        # Derive the AES keys
        aes_key1, aes_key2 = self.__derive_aes_keys(salt, passphrase)

        # Initialize the AES-XTS cipher for decryption
        cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(TWEAK))
        decryptor = cipher.decryptor()

        # Decrypt the volume (excluding the salt)
        decrypted_data = decryptor.update(encrypted_volume[64:]) + decryptor.finalize()

        # Verify the magic number 'TRUE' in the decrypted header
        if decrypted_data[:4] != b"TRUE":
            print("Error: Magic number 'TRUE' not found. Decryption failed.")

            # Return an None Type
            return None

        # Return the decrypted data, including the salt
        return salt + decrypted_data

    def __encrypt_volume(self, salty: bytes, decrypted_volume: bytes, passphrase: str) -> bytes:
        """
        Encrypts the provided decrypted volume using AES-XTS with the given salt.

        Parameters:
        salty (bytes): The salt used for encryption.
        decrypted_volume (bytes): The decrypted TrueCrypt volume data.
        passphrase (str): The passphrase for encryption.

        Returns:
        bytes: The encrypted volume, including the salt.
        """
        # Derive the AES keys using the salt
        aes_key1, aes_key2 = self.__derive_aes_keys(salty, passphrase)

        # Initialize the AES-XTS cipher for encryption
        cipher = Cipher(algorithms.AES(aes_key1 + aes_key2), modes.XTS(TWEAK))
        encryptor = cipher.encryptor()

        # Encrypt the volume (excluding the salt)
        encrypted_data = encryptor.update(decrypted_volume[64:]) + encryptor.finalize()

        # Return the encrypted data, including the salt
        return salty + encrypted_data
