from Engine.plugin_Interface import plugin_Interface
import struct
# Kommentar Fabian: Skript angepasst so dass ich tatsächlich auch BYTES erhalte
class Wav(plugin_Interface):
    def run(self, truecrypt, wav_host):
        # Die Größe des Volume ermitteln
        volume_size = len(truecrypt)

        # Aktuelle Host-Dateigröße aus den Bytes 4-7 lesen und um volume_size erhöhen
        wav_host_size = struct.unpack_from('>I', wav_host, 4)[0]  # '>I' steht für Big-Endian 32-Bit Integer
        new_host_size = wav_host_size + volume_size

        # Die neue Größe in den Header (Bytes 4-7) schreiben
        updated_host_data = bytearray(wav_host)  # In ein veränderbares bytearray konvertieren
        struct.pack_into('>I', updated_host_data, 4, new_host_size)

        # Host-Datei bis zum Einfügepunkt (Byte 35) und ab Einfügepunkt trennen
        before_insert = bytes(updated_host_data[:35])  # Convert to bytes here
        after_insert = bytes(updated_host_data[35:])  # Convert to bytes here

        updated_guest_data = bytes(truecrypt[35:])  # Convert guest data to bytes if necessary

        # Zusammensetzen der neuen Datei: Vor dem Einfügepunkt + Guest-Datei + Rest der Host-Datei
        polyglott = before_insert + updated_guest_data + after_insert

        # Ensure polyglott is of type bytes
        return bytes(polyglott)
