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



class CLI():
    def __init__(self, verbose):

        self.verbose = verbose


    def display_message(self, message, message_type):

        # ANSI color codes
        colors = {
            "info": "\033[34m",  # Blue
            "verbose": "\033[32m",  # Green
            "error": "\033[31m",  # Red
            "message": "\033[37m",  # White
            "reset": "\033[0m",  # Reset to default
            "unknown": "\033[35m",  # Purple for unknown message types
        }

        # Choose the color based on the message type
        color = colors.get(message_type, colors["unknown"])

        if message_type == "info":
            print(f"{color}[INFO] {message}{colors['reset']}")
        elif message_type == "verbose":
            if self.verbose:
                print(f"{color}[VERBOSE] {message}{colors['reset']}")
        elif message_type == "error":
            print(f"{color}[ERROR] {message}{colors['reset']}")
        elif message_type == "message":
            print(f"{color}{message}{colors['reset']}")
        else:
            print(f"{color}[UNKNOWN] {message}{colors['reset']}")
