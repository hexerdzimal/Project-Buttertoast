from Engine.plugin_Interface import plugin_Interface
import struct

class Ico(plugin_Interface):
    def run(self, truecrypt, ico_host):
        atom_size = struct.pack('>I', len(truecrypt))
        atom_type = b'skip'
        major_brand = b'isom'
        minor_version = b'\x00\x00\x00\x01'
        compatible_brands = b'isomiso2avc1mp41'[:12]
        skip_atom_salt = atom_size + atom_type + major_brand + minor_version + compatible_brands
        skip_atom_salt += b'\x00' * (SALT_SIZE - len(skip_atom_salt))
        polyglott = skip_atom_salt + truecrypt[65:] + mov_host
        stco_index = polyglott.find(b'stco')
        offset_count_index = stco_index + 8
        offset_count = struct.unpack(">I", data[offset_count_index:offset_count_index + 4])[0]
        offset_table_index = offset_count_index + 4

        for i in range(offset_count):
            current_offset_index = offset_table_index + (i * 4)
            current_offset = struct.unpack(">I", data[current_offset_index:current_offset_index + 4])[0]
            adjusted_offset = current_offset + skip_atom_size
            polyglott[current_offset_index:current_offset_index + 4] = adjusted_offset

        return polyglott