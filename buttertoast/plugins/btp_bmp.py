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
    def run(self, truecrypt, bmp_host):
        polyglot = bytearray(truecrypt) + bytearray(bmp_host)
        bmp_header = bmp_host[:54]
        bfOffBits_position = 10
        new_bfOffBits = len(truecrypt)
        modified_bmp_header = (
                bmp_header[:bfOffBits_position] +
                struct.pack('<I', new_bfOffBits) +
                bmp_header[bfOffBits_position + 4:]
        )
        salt = modified_bmp_header + b'\x00' * (64 - len(modified_bmp_header))
        polyglot = bytes(bytearray(salt) + bytearray(polyglot[64:]))
        return polyglot