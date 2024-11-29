from Engine.plugin_Interface import plugin_Interface
import struct

class Zip(plugin_Interface):
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