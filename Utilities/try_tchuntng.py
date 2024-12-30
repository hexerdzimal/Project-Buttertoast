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
        ui.display_message(f"'tchuntng' was executed. Exit code: {result.returncode}", "info")
        return result.returncode
    except Exception as e:
        print(f"Error while executing 'tchuntng': {e}")
        return None
