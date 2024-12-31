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


from Engine.plugin_Interface import plugin_Interface

class Filetype(plugin_Interface):
    """
    The `Html` class is a plugin for creating polyglot files by embedding a TrueCrypt volume within an HTML file.

    This plugin inserts the TrueCrypt volume as a comment block within the provided HTML host file, ensuring that the HTML remains valid while incorporating the encrypted volume data. The TrueCrypt volume is embedded after the first `>` character in the HTML content.

    Methods:
        - `run(truecrypt: bytes, html_host: bytes) -> bytes`:
            Accepts the TrueCrypt volume and the HTML host file as byte inputs, modifies the HTML file to include the TrueCrypt volume as a comment block, and returns the resulting polyglot file.

    Parameters:
        - `truecrypt` (bytes): The encrypted TrueCrypt volume to be embedded.
        - `html_host` (bytes): The HTML file into which the TrueCrypt volume will be embedded.

    Returns:
        - `polyglott` (bytes): A modified HTML file containing the TrueCrypt volume embedded as a comment block.

    Example:
        ```python
        html_plugin = Html()
        polyglot = html_plugin.run(truecrypt_volume, html_file)
        with open("output.html", "wb") as f:
            f.write(polyglot)
        ```
    """
    def run(self, truecrypt, html_host):        
        offset = html_host.find(b'>')
        comment_start = (b'<!--')
        comment_end = (b'//-->')    
        polyglott = html_host[:offset+1] + comment_start + truecrypt[offset+5:] + comment_end + html_host[1+offset:]

        return polyglott