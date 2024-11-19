from Engine.plugin_Interface import plugin_Interface
import struct
import zlib


class Png(plugin_Interface):

    def crc_berechnen(self, data):
        """CRC eines Datenchunks berechnen"""
        # Invertierte CRC Checksumme zum Anfügen an den Chunk berechnen
        return zlib.crc32(data) & 0xffffffff

    def run(self, truecrypt, png_host):
        # Chunk zusammenstellen
        chunk_type = b'buTt'
        chunk_data = truecrypt[41:]
        chunk_length = len(chunk_data)
        chunk_crc = self.crc_berechnen(chunk_type + chunk_data)  # Call the crc_berechnen method

        # Chunk formatieren [length][type][data][CRC]
        custom_chunk = struct.pack(f'!I4s{chunk_length}sI', chunk_length, chunk_type, chunk_data, chunk_crc)

        # Hinter IHDR chunk einfügen
        polyglott = png_host[:33] + custom_chunk + png_host[33:]

        return polyglott
