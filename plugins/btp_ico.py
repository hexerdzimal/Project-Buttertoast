from Engine.plugin_Interface import plugin_Interface
import struct

class Ico(plugin_Interface):
    def run(self, truecrypt, ico_host):
        # ICO-Header und Icon Directory Entry extrahieren
        ico_header = ico_host[:6]  # Die ersten 6 Bytes der ICO-Datei
        icon_directory_entry = ico_host[6:22]  # Nächste 16 Bytes für das Icon Directory Entry

        # Neuen Image Offset berechnen
        new_image_offset = len(truecrypt) + 8  # Länge der TrueCrypt-Daten + Padding
        modified_icon_directory_entry = (
                icon_directory_entry[:12] +
                struct.pack('<I', new_image_offset)  # Neuer Offset
        )

        # Padding definieren
        padding = b'\x00' * 8

        # Originale Bilddaten aus der ICO-Datei extrahieren
        image_offset = struct.unpack('<I', icon_directory_entry[12:16])[0]
        ico_image_data = ico_host[image_offset:]

        # Polyglot-Datei zusammenstellen
        polyglot = (
                ico_header +
                modified_icon_directory_entry +
                truecrypt[22:] +
                padding +
                ico_image_data
        )
        return polyglot