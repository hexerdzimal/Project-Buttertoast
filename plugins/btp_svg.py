from Engine.plugin_Interface import plugin_Interface

class Svg(plugin_Interface):
    """
    The `Svg` class is a plugin for creating polyglot files by embedding a TrueCrypt volume into an SVG file.

    This plugin modifies the SVG file structure by adding a comment block that contains the TrueCrypt volume data.
    The resulting polyglot file remains a valid SVG file while also embedding the TrueCrypt volume.

    Methods:
        - `run(truecrypt: bytes, svg_host: bytes) -> bytes`: Embeds the TrueCrypt volume into the SVG host file and returns the modified polyglot file.

    Parameters:
        - `truecrypt` (bytes): The encrypted TrueCrypt volume to be embedded.
        - `svg_host` (bytes): The SVG file into which the TrueCrypt volume will be embedded.

    Returns:
        - `polyglot` (bytes): The modified SVG file containing the TrueCrypt volume.

    Example:
        ```python
        svg_plugin = Svg()
        polyglot = svg_plugin.run(truecrypt_volume, svg_file)
        with open("output.svg", "wb") as f:
            f.write(polyglot)
        ```
    """

    def run(self, truecrypt, svg_host):
        """
        Embeds the TrueCrypt volume into the SVG file as a comment block.

        The TrueCrypt volume data is inserted as a comment block (`<!-- ... //-->`) into the SVG host file.
        The insertion occurs immediately after the first `>` character in the SVG file.

        Parameters:
            - `truecrypt` (bytes): The encrypted TrueCrypt volume to embed.
            - `svg_host` (bytes): The SVG host file to modify.

        Returns:
            - `polyglot` (bytes): The resulting SVG file with the embedded TrueCrypt volume.
        """
        # Find the position of the first '>' character in the SVG host
        offset = svg_host.find(b'>')

        # Define the start and end of the comment block
        comment_start = b'<!--'  # Start of the comment block
        comment_end = b'//-->'   # End of the comment block

        # Create the polyglot file by inserting the TrueCrypt volume as a comment block
        polyglot = (
            svg_host[:offset + 1] +  # Everything up to and including the first '>'
            comment_start +          # Insert the start of the comment block
            truecrypt[offset + 5:] + # Insert the TrueCrypt volume data (adjusting for offset)
            comment_end +            # Insert the end of the comment block
            svg_host[1 + offset:]    # Add the remaining SVG file content
        )

        return polyglot
