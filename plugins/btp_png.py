from Engine.plugin_Interface import plugin_Interface
import struct

class Png(plugin_Interface):
    
    def run(self, truecrypt, png_host):
        
        # Chunk zusammenstellen
        chunk_type=b'buTt'
        chunk_data = truecrypt[41:]
        chunk_length = len(chunk_data)
        chunk_crc = crc_berechnen(chunk_type + chunk_data)
        
        # Chunk formatieren [length][type][data][CRC]
        custom_chunk = struct.pack(f'!I4s{chunk_length}sI', chunk_length, chunk_type, chunk_data, chunk_crc)
        
        # Hinter IHDR chunk einfügen
        polyglott = png_host[:33] + custom_chunk + png_host[33:]
        
        def crc_berechnen(data):
            #invertierte CRC Checksumme zum Anfügen an den Chunk berechnen
            """CRC eines Datenchunks berechnen"""
            import zlib
            return zlib.crc32(data) & 0xffffffff

        return polyglott
    
