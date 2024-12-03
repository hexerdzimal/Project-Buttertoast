from Engine.plugin_Interface import plugin_Interface
import struct

class Bmp(plugin_Interface):
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