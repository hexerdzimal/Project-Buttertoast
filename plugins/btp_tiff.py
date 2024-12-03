from Engine.plugin_Interface import plugin_Interface
import struct

class Tiff(plugin_Interface):
    """
    The `Tiff` class is a plugin for creating polyglot files by embedding a TrueCrypt volume into a TIFF file.

    This plugin modifies the TIFF file structure by embedding the TrueCrypt volume into the TIFF's binary data.
    Additionally, it adjusts all necessary offsets in the TIFF structure to ensure the resulting file remains valid.

    Methods:
        - `run(truecrypt: bytes, tiff_host: bytes) -> bytes`: Embeds the TrueCrypt volume into the TIFF host file and returns the modified polyglot file.

    Parameters:
        - `truecrypt` (bytes): The encrypted TrueCrypt volume to be embedded.
        - `tiff_host` (bytes): The TIFF file into which the TrueCrypt volume will be embedded.

    Returns:
        - `polyglott` (bytes): The modified TIFF file containing the embedded TrueCrypt volume.

    Example:
        ```python
        tiff_plugin = Tiff()
        polyglot = tiff_plugin.run(truecrypt_volume, tiff_file)
        with open("output.tiff", "wb") as f:
            f.write(polyglot)
        ```
    """

    def run(self, truecrypt, tiff_host):
        """
        Embeds the TrueCrypt volume into the TIFF file and adjusts all relevant offsets.

        The TrueCrypt volume is inserted after the initial 8 bytes of the TIFF file.
        All offsets within the TIFF structure are adjusted to account for the additional TrueCrypt volume.

        Parameters:
            - `truecrypt` (bytes): The encrypted TrueCrypt volume to embed.
            - `tiff_host` (bytes): The TIFF host file to modify.

        Returns:
            - `polyglott` (bytes): The resulting TIFF file with the embedded TrueCrypt volume.
        """
        # Extract the TrueCrypt volume data starting from the 8th byte
        rest_of_crypt = truecrypt[8:]
        crypt_length = len(rest_of_crypt)

        # Determine byte order (little-endian or big-endian) based on TIFF header
        byte_order = tiff_host[:2].decode()
        endian = '<' if byte_order == 'II' else '>'  # 'II' means little-endian, 'MM' means big-endian

        # Combine the TIFF header, TrueCrypt volume data, and the rest of the TIFF file
        polyglott = (
            bytearray(tiff_host[:8]) +  # TIFF header
            bytearray(rest_of_crypt) +  # Embedded TrueCrypt volume
            bytearray(tiff_host[8:])    # Remaining TIFF data
        )

        # Define a function to find all offsets within the TIFF structure
        def find_offsets(polyglott, ifd_offset, endian):
            """
            Finds all offsets in the TIFF structure that point to large data chunks.

            Parameters:
                - `polyglott` (bytearray): The modified TIFF data.
                - `ifd_offset` (int): The starting offset of the first IFD (Image File Directory).
                - `endian` (str): The byte order ('<' for little-endian, '>' for big-endian).

            Returns:
                - `offsets` (list): A list of offsets that need to be adjusted.
            """
            offsets = []
            while ifd_offset != 0:
                # Prevent reading beyond the bounds of the file
                if ifd_offset + 2 > len(polyglott):
                    break

                # Read the number of entries in the current IFD
                num_entries = struct.unpack(endian + 'H', polyglott[ifd_offset:ifd_offset + 2])[0]

                # Iterate through all tags in the IFD
                for i in range(num_entries):
                    tag_start = ifd_offset + 2 + 12 * i
                    if tag_start + 12 > len(polyglott):
                        break

                    # Read the tag data
                    tag_data = polyglott[tag_start:tag_start + 12]
                    tag_id, data_type, value_count, value_or_offset = struct.unpack(endian + 'HHII', tag_data)

                    # If the data size exceeds 4 bytes, store the offset
                    if value_count * struct.calcsize('I') > 4:
                        offsets.append(value_or_offset)

                # Find the next IFD offset (4 bytes after the entries)
                next_ifd_offset_start = ifd_offset + 2 + 12 * num_entries
                if next_ifd_offset_start + 4 > len(polyglott):
                    break
                ifd_offset = struct.unpack(endian + 'I', polyglott[next_ifd_offset_start:next_ifd_offset_start + 4])[0]

            return offsets

        # Start finding offsets from the first IFD (Image File Directory)
        first_ifd_offset = struct.unpack(endian + 'I', tiff_host[4:8])[0]
        offsets = find_offsets(polyglott, first_ifd_offset, endian)

        # Adjust all found offsets to account for the added TrueCrypt volume
        for offset in offsets:
            # Locate the position of the offset in the TIFF data
            offset_position = polyglott.find(struct.pack(endian + 'I', offset))
            if offset_position != -1:
                # Calculate the new offset
                new_offset = offset + crypt_length
                # Update the offset in the TIFF data
                polyglott[offset_position:offset_position + 4] = struct.pack(endian + 'I', new_offset)

        return polyglott
