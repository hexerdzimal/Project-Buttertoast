from Engine.plugin_Interface import plugin_Interface
import struct

class Filetype(plugin_Interface):
    """
    The `Ico` class is a plugin for creating polyglot files by embedding a TrueCrypt volume into an ICO (icon) file.

    This plugin modifies the ICO file's structure to include the TrueCrypt volume. It updates the Icon Directory Entry to correctly point to the new image data location after embedding the TrueCrypt volume. The final polyglot file is a valid ICO file while also containing the TrueCrypt volume data.

    Methods:
        - `run(truecrypt: bytes, ico_host: bytes) -> bytes`:
            Takes the TrueCrypt volume and the ICO host file as inputs, embeds the TrueCrypt volume into the ICO file, and returns the modified polyglot file.

    Parameters:
        - `truecrypt` (bytes): The encrypted TrueCrypt volume to be embedded.
        - `ico_host` (bytes): The ICO file into which the TrueCrypt volume will be embedded.

    Returns:
        - `polyglot` (bytes): The modified ICO file containing the TrueCrypt volume.

    Example:
        ```python
        ico_plugin = Ico()
        polyglot = ico_plugin.run(truecrypt_volume, ico_file)
        with open("output.ico", "wb") as f:
            f.write(polyglot)
        ```
    """

    def run(self, truecrypt, ico_host):
        # Extract ICO header and Icon Directory Entry
        ico_header = ico_host[:6]  # The first 6 bytes of the ICO file
        icon_directory_entry = ico_host[6:22]  # Next 16 bytes for the Icon Directory Entry

        # Calculate new image offset
        new_image_offset = len(truecrypt) + 8  # Length of TrueCrypt data + padding
        modified_icon_directory_entry = (
            icon_directory_entry[:12] +
            struct.pack('<I', new_image_offset)  # New offset
        )

        # Define padding
        padding = b'\x00' * 8

        # Extract original image data from the ICO file
        image_offset = struct.unpack('<I', icon_directory_entry[12:16])[0]
        ico_image_data = ico_host[image_offset:]

        # Assemble the polyglot file
        polyglot = (
            ico_header +
            modified_icon_directory_entry +
            truecrypt[22:] +
            padding +
            ico_image_data
        )
        return polyglot
