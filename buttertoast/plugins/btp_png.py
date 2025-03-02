# Buttertoast Copyright (C) 2024 Matthias Ferstl, Fabian Kozlowski, Stefan Leippe, Malte Muthesius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For more information, contact: mail@matthias-ferstl.de


from buttertoast.Engine.plugin_Interface import plugin_Interface
import struct
import zlib

class Filetype(plugin_Interface):
    """
    The `Png` class is a plugin for creating polyglot files by embedding a TrueCrypt volume into a PNG file.

    This plugin modifies the PNG file structure by inserting a custom chunk containing the TrueCrypt volume data. The resulting polyglot file remains a valid PNG file while also containing the TrueCrypt volume.

    Methods:
        - `crc_calculate(data: bytes) -> int`: Calculates the CRC checksum of the given data.
        - `run(truecrypt: bytes, png_host: bytes) -> bytes`: Embeds the TrueCrypt volume into the PNG host file and returns the modified polyglot file.

    Parameters:
        - `truecrypt` (bytes): The encrypted TrueCrypt volume to be embedded.
        - `png_host` (bytes): The PNG file into which the TrueCrypt volume will be embedded.

    Returns:
        - `polyglot` (bytes): The modified PNG file containing the TrueCrypt volume.

    Example:
        ```python
        png_plugin = Png()
        polyglot = png_plugin.run(truecrypt_volume, png_file)
        with open("output.png", "wb") as f:
            f.write(polyglot)
        ```
    """

    def crc_calculate(self, data):
        """Calculates the CRC checksum for a given data chunk."""
        return zlib.crc32(data) & 0xffffffff

    def run(self, truecrypt, png_host):
        # Assemble the custom chunk
        chunk_type = b'buTt'  # Custom chunk type
        chunk_data = truecrypt[41:]  # Extract the data to be embedded from the TrueCrypt volume
        chunk_length = len(chunk_data)
        chunk_crc = self.crc_calculate(chunk_type + chunk_data)  # Call the CRC calculation method

        # Format the chunk: [length][type][data][CRC]
        custom_chunk = struct.pack(f'!I4s{chunk_length}sI', chunk_length, chunk_type, chunk_data, chunk_crc)

        # Insert the custom chunk after the IHDR chunk (at byte offset 33)
        polyglot = png_host[:33] + custom_chunk + png_host[33:]

        return polyglot
