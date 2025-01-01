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

class Filetype(plugin_Interface):
    def run(self, truecrypt, zip_host):
        polyglot = bytearray(truecrypt) + bytearray(zip_host)
        polyglot = bytes(polyglot)
        eocd_signature = b'\x50\x4b\x05\x06'
        eocd_index = polyglot.find(eocd_signature)
        central_offset_position = eocd_index + 16
        central_offset = struct.unpack("<I", polyglot[central_offset_position:central_offset_position + 4])[0]
        new_central_offset = central_offset + len(truecrypt)
        polyglot = (
                polyglot[:central_offset_position]
                + struct.pack("<I", new_central_offset)
                + polyglot[central_offset_position + 4:]
        )
        return polyglot