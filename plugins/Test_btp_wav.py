from Engine.plugin_Interface import plugin_Interface
import struct

# Das ist die aktualisierte Version mit dem Bugfix
class Wav(plugin_Interface):
    def run(self, truecrypt, wav_host):
        # WAV parts
        riff_header = wav_host[:4]
        file_size_bytes = wav_host[4:8]
        rest_of_header = wav_host[8:28]
        rest_of_data = wav_host[28:]

        # TrueCrypt parts
        chunk_data = truecrypt[36:]
        chunk_id = 'INFO'
        chunk_id = chunk_id.ljust(4)[:4]  # ID padding
        chunk_size = len(chunk_data)

        # make custom chunk
        custom_chunk = struct.pack(f'4sI{chunk_size}s', chunk_id.encode('ascii'), chunk_size, chunk_data)

        # read file size, add crypt size
        current_file_size = struct.unpack('<I', file_size_bytes)[0]  # '<I' for Little-Endian 32-Bit Integer
        new_file_size = current_file_size + len(custom_chunk)

        # write back new file size
        new_file_size_bytes = struct.pack('<I', new_file_size)

        # combine data in wav structure
        # Bytes 0-3 riff header
        # Bytes 4-7 new file size bytes
        # Bytes 8-27 der restliche WAV header
        # Bytes 28-64 chunk data
        polyglott = riff_header + new_file_size_bytes + rest_of_header + custom_chunk + rest_of_data

        return polyglott