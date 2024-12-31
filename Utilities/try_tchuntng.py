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


import subprocess
import shutil

def check_tchuntng():
    """
    Checks if the 'tchuntng' command is available in the PATH and executable.

    Returns:
        bool: True if 'tchuntng' is found, otherwise False.
    """
    # Check if 'tchuntng' is available in the PATH
    if not shutil.which("tchuntng"):
        return False
    return True

def run_tchuntng(file_path, ui):
    """
    Executes 'tchuntng' with the given file path if it is available in the PATH.

    Args:
        file_path (str): The path to the file to be checked by 'tchuntng'.

    Returns:
        int or None: The exit code of the 'tchuntng' command, or None in case of errors.
    """
    # Check and execute
    if not check_tchuntng():
        ui.display_message(f"'tchuntng' is not available in the PATH or is not executable.", "error")
        return None

    try:
        # Execute 'tchuntng' with the file path
        result = subprocess.run(["tchuntng", file_path], check=False)

        # Write to log
        ui.display_message(f"'tchuntng' was executed. Exit code: {result.returncode}", "verbose")
        
        # Display the exit code and corresponding message
        if result.returncode == 0:
            ui.display_message("File generated, but 'tchuntng' recognizes it as '...likely to be encrypted.'", "error")
        elif result.returncode == 1:
            ui.display_message("A generic error occurred while running 'tchuntng'.", "error")
        elif result.returncode == 2:
            ui.display_message(f"File successfully generated.
                               'tchuntng' recognizes file as 'not encrypted!'", "info")
        elif result.returncode == 3:
            ui.display_message("The operation was interrupted by a signal.", "error")
        else:
            ui.display_message(f"Unexpected exit code: {result.returncode}", "error")

 
        return result.returncode
    except Exception as e:
        print(f"Error while executing 'tchuntng': {e}")
        ui.display_message("An error occurred while executing 'tchuntng'.", "error")
        return None
