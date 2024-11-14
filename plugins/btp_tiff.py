from Engine.plugin_Interface import plugin_Interface
import struct

class Tiff(plugin_Interface):    
    def run(self, truecrypt, tiff_host):
        rest_of_crypt = truecrypt[8:]
        crypt_length = len(rest_of_crypt)
        byte_order = tiff_host[:2].decode()
        endian = '<' if byte_order == 'II' else '>'

        polyglott = bytearray(tiff_host[:8]) + bytearray(rest_of_crypt) + bytearray(tiff_host[8:])
        
        # Funktion, um alle relevanten Offsets in einer TIFF-Struktur zu finden
        def find_offsets(polyglott, ifd_offset, endian):
            offsets = []
            while ifd_offset != 0:
                # Verhindert das Lesen außerhalb des Datei-Arrays
                if ifd_offset + 2 > len(polyglott):
                    break

                # Anzahl der Einträge im aktuellen IFD
                num_entries = struct.unpack(endian + 'H', polyglott[ifd_offset:ifd_offset + 2])[0]
                
                # Durchlaufe alle Tags im IFD
                for i in range(num_entries):
                    tag_start = ifd_offset + 2 + 12 * i
                    if tag_start + 12 > len(polyglott):
                        break

                    # Lese Tag-Daten
                    tag_data = polyglott[tag_start:tag_start + 12]
                    tag_id, data_type, value_count, value_or_offset = struct.unpack(endian + 'HHII', tag_data)

                    # Prüfe, ob ein Offset zu großen Daten führt (mehr als 4 Byte), dann speichere es
                    if value_count * struct.calcsize('I') > 4:
                        offsets.append(value_or_offset)

                # Nächster IFD-Offset (4 Bytes nach den Einträgen)
                next_ifd_offset_start = ifd_offset + 2 + 12 * num_entries
                if next_ifd_offset_start + 4 > len(polyglott):
                    break
                ifd_offset = struct.unpack(endian + 'I', polyglott[next_ifd_offset_start:next_ifd_offset_start + 4])[0]

            return offsets

        # Starte die Offset-Suche vom ersten IFD aus
        first_ifd_offset = struct.unpack(endian + 'I', tiff_host[4:8])[0]
        offsets = find_offsets(polyglott, first_ifd_offset, endian)
        
        # Offsets anpassen
        for offset in offsets:
            offset_position = polyglott.find(struct.pack(endian + 'I', offset))
            if offset_position != -1:
                new_offset = offset + crypt_length
                polyglott[offset_position:offset_position + 4] = struct.pack(endian + 'I', new_offset)

        return polyglott