# Buttertoast Copyright (C) 2024 Matthias Ferstl, Fabian Kozlowski, Stefan Leippe, Malte Muthesius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For more information, contact: mail@matthias-ferstl.de


def compare_files():
    # Pfade der beiden Dateien eingeben und Anführungszeichen entfernen
    file1_path = input("Geben Sie den Pfad zur ersten Datei ein: ").strip().strip('"')
    file2_path = input("Geben Sie den Pfad zur zweiten Datei ein: ").strip().strip('"')

    try:
        with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
            file1_data = file1.read()
            file2_data = file2.read()

        if file1_data == file2_data:
            print("Die Dateien sind identisch.")
        else:
            print("Die Dateien sind unterschiedlich.")
            min_length = min(len(file1_data), len(file2_data))
            for i in range(min_length):
                if file1_data[i] != file2_data[i]:
                    print(f"Unterschied an Byte {i}: Datei 1 = {file1_data[i]:02x}, Datei 2 = {file2_data[i]:02x}")
            if len(file1_data) > min_length:
                print(f"Zusätzliche Daten in Datei 1 ab Byte {min_length}.")
            elif len(file2_data) > min_length:
                print(f"Zusätzliche Daten in Datei 2 ab Byte {min_length}.")
    except FileNotFoundError as e:
        print(f"Dateifehler: {e}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Vergleich starten
compare_files()
