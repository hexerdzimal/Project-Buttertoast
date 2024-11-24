from Engine.plugin_Interface import plugin_Interface
import struct

class Tiff(plugin_Interface):    
    def run(self, truecrypt, tiff_host):
        rest_of_crypt = truecrypt[8:]
        crypt_length = len(rest_of_crypt)
        byte_order = tiff_host[:2].decode()
        endian = '<' if byte_order == 'II' else '>'

        polyglott = bytearray(tiff_host[:8]) + bytearray(rest_of_crypt) + bytearray(tiff_host[8:])

            def find_and_adjust_offsets(polyglott, ifd_offset, endian, adjustment):

                while ifd_offset != 0:

                    # read number of ifd entries
                    num_entries = struct.unpack(endian + 'H', polyglott[ifd_offset:ifd_offset + 2])[0]

                    for i in range(num_entries):
                        tag_start = ifd_offset + 2 + 12 * i

                        # read tag data
                        tag_data = polyglott[tag_start:tag_start + 12]
                        tag_id, data_type, value_count, value_or_offset = struct.unpack(endian + 'HHII', tag_data)

                        # check tag for offset
                        if value_count * struct.calcsize('I') > 4:
                            offset_position = tag_start + 8
                            offset_value = struct.unpack(endian + 'I', polyglott[offset_position:offset_position + 4])[
                                0]

                            # adjust offset
                            new_offset = offset_value + adjustment
                            polyglott[offset_position:offset_position + 4] = struct.pack(endian + 'I', new_offset)

                    # read next offset
                    next_ifd_offset_start = ifd_offset + 2 + 12 * num_entries
                    if next_ifd_offset_start + 4 > len(polyglott):
                        break
                    next_ifd_offset = \
                    struct.unpack(endian + 'I', polyglott[next_ifd_offset_start:next_ifd_offset_start + 4])[0]

                    # adjust next offset
                    if next_ifd_offset != 0:
                        adjusted_next_ifd_offset = next_ifd_offset + adjustment
                        polyglott[next_ifd_offset_start:next_ifd_offset_start + 4] = struct.pack(endian + 'I',
                                                                                                 adjusted_next_ifd_offset)

                    # recurse through offsets
                    ifd_offset = next_ifd_offset

            # start with first IFD-Offset
            first_ifd_offset = struct.unpack(endian + 'I', tiff_host[4:8])[0]

            # first adjusted IFD-Offset
            adjusted_ifd_offset = first_ifd_offset + crypt_length
            polyglott[4:8] = struct.pack(endian + 'I', adjusted_ifd_offset)

            # Adjust Offsets
            find_and_adjust_offsets(polyglott, adjusted_ifd_offset, endian, crypt_length)

            return polyglott