from Engine.plugin_Interface import plugin_Interface
import struct

class Wav(plugin_Interface):
    """
    The `Wav` class is a plugin for creating polyglot files by embedding a TrueCrypt volume into a WAV file.

    This plugin modifies the WAV file structure by adding a custom chunk that contains the TrueCrypt volume.
    Additionally, it updates the file size in the WAV header to reflect the added data.

    Methods:
        - `run(truecrypt: bytes, wav_host: bytes) -> bytes`: Embeds the TrueCrypt volume into the WAV host file and returns the modified polyglot file.

    Parameters:
        - `truecrypt` (bytes): The encrypted TrueCrypt volume to be embedded.
        - `wav_host` (bytes): The WAV file into which the TrueCrypt volume will be embedded.

    Returns:
        - `polyglot` (bytes): The modified WAV file containing the embedded TrueCrypt volume.

    Example:
        ```python
        wav_plugin = Wav()
        polyglot = wav_plugin.run(truecrypt_volume, wav_file)
        with open("output.wav", "wb") as f:
            f.write(polyglot)
        ```
    """

    def run(self, truecrypt, wav_host):
        """
        Embeds the TrueCrypt volume into the WAV file and adjusts the file size in the header.

        The TrueCrypt volume is inserted as a custom chunk into the WAV file. The file size in the WAV header
        is updated to reflect the additional data.

        Parameters:
            - `truecrypt` (bytes): The encrypted TrueCrypt volume to embed.
            - `wav_host` (bytes): The WAV host file to modify.

        Returns:
            - `polyglot` (bytes): The resulting WAV file with the embedded TrueCrypt volume.
        """
        # Extract parts of the WAV file
        riff_header = wav_host[:4]  # "RIFF" header (first 4 bytes)
        file_size_bytes = wav_host[4:8]  # Current file size (bytes 4-8)
        rest_of_header = wav_host[8:36]  # Remaining header data
        rest_of_data = wav_host[36:]  # Audio data and other chunks

        # Extract data from the TrueCrypt volume
        chunk_data = truecrypt[44:]  # Skip the first 44 bytes of the TrueCrypt volume
        chunk_id = 'info'  # Custom chunk ID
        chunk_id = chunk_id.ljust(4)[:4]  # Ensure the chunk ID is exactly 4 bytes (padded if necessary)
        chunk_size = len(chunk_data)  # Size of the custom chunk

        # Create a custom chunk using the TrueCrypt data
        custom_chunk = struct.pack(
            f'4sI{chunk_size}s',  # Format: 4 bytes for chunk ID, 4 bytes for chunk size, variable length for chunk data
            chunk_id.encode('ascii'),  # Encode chunk ID as ASCII
            chunk_size,  # Size of the chunk
            chunk_data  # Chunk data (from the TrueCrypt volume)
        )

        # Read the current file size from the WAV header
        current_file_size = struct.unpack('<I', file_size_bytes)[0]  # '<I' indicates Little-Endian 32-bit Integer
        new_file_size = current_file_size + len(custom_chunk)  # Update the file size by adding the custom chunk size

        # Pack the new file size back into the WAV header
        new_file_size_bytes = struct.pack('<I', new_file_size)

        # Combine all parts of the WAV file into the polyglot
        polyglot = (
            riff_header +  # RIFF header
            new_file_size_bytes +  # Updated file size
            rest_of_header +  # Remaining WAV header
            custom_chunk +  # Custom chunk containing the TrueCrypt volume
            rest_of_data  # Remaining WAV data
        )

        return polyglot
