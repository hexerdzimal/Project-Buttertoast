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

from buttertoast.UI.BaseUI import BaseUI
import getpass
import importlib.resources
from rich.console import Console
from rich.markdown import Markdown

class TUI(BaseUI):
    def __init__(self, engine, event_manager):
        """
        Initialize the TUI (Text User Interface) with an event manager.
        
        Args:
            event_manager: The event manager responsible for triggering events in the application.
        """
        super().__init__(engine)
        self.event_manager = event_manager

    def display_title(self):
        """
        Displays the title of the application only once.
        This method is called at the start of the application to display the logo and version.
        """
        print(r"""
            +===================================================================================================+
            |                                                                                                   |
            |   ██████╗ ██╗   ██╗████████╗████████╗███████╗██████╗ ████████╗ ██████╗  █████╗ ███████╗████████╗  |
            |   ██╔══██╗██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝  |
            |   ██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝   ██║   ██║   ██║███████║███████╗   ██║     |
            |   ██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗   ██║   ██║   ██║██╔══██║╚════██║   ██║     |
            |   ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║███████║   ██║     |
            |   ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝     |
            |                                   The melting pot for polyglot.                                   |
            +===================================================================================================+
            Copyright (C) 2024 Matthias Ferstl, Fabian Kozlowski, Stefan Leippe, Malte Muthesius
            This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
            This program comes with ABSOLUTELY NO WARRANTY; 
            This is free software, and you are welcome to redistribute it under certain conditions;
            For more information, contact: mail@matthias-ferstl.de
                """)

    def run(self):
        """
        Displays the main menu and allows the user to choose actions like starting data input, listing plugins, or adjusting settings.
        This method also handles user navigation in the menu.
        """
        self.display_title()  # Display the title once at the start
        self.console = Console()

        while True:
            print("\n")
            print("Main Menu")
            print("------------------------------------------")
            print("1: Start data input and processing")
            print("2: List plugins")
            print("3: Settings")
            print("4: View Documentation")  
            print("5: Exit")  
            print("\n")

            choice = input("Please choose an option: ").strip()

            if choice == "1":
                self.data_input_menu()  # Navigate to data input menu
            elif choice == "2":
                self.trigger_list_data()  # Trigger the list data event
            elif choice == "3":
                self.edit_config()  # Navigate to the settings menu
            elif choice == "4":
                self.show_documentation_menu()  # Show documentation menu
            elif choice == "5":
                print("Goodbye!")
                break  # Exit the application
            else:
                self.display_message("Invalid selection. Please try again.", "error")

    def data_input_menu(self):
        """
        Guides the user through the data input process where they first provide all necessary information (host, volume, 
        password, and output file path), and then allows them to modify specific fields or trigger the 'process_data' event.
        """
        # Step 1: Directly ask for all required fields
        print("\nEnter the required file paths and password.")
        host = input("Host file path: ").strip()
        volume = input("Volume file path: ").strip()
        password = getpass.getpass("Password: ").strip()
        output = input("Output file path: ").strip()

        while True:
            # Step 2: Show the options to modify individual fields or start the processing
            print("\nCurrent Settings")
            print("------------------------------------------")
            print(f"1: Host file path: {host}")
            print(f"2: Volume file path: {volume}")
            print(f"3: Password: {'*****' if password else 'Not Set'}")
            print(f"4: Output file path: {output}")
            print("\n")
            print("5: Start data processing")
            print("6: Cancel and restart")
            print("\n")

            choice = input("Please choose an option (you can change your input or start/cancel the process): ").strip()

            if choice == "1":
                host = input("Enter the host file path: ").strip()
            elif choice == "2":
                volume = input("Enter the volume file path: ").strip()
            elif choice == "3":
                password = input("Enter the password: ").strip()
            elif choice == "4":
                output = input("Enter the output file path: ").strip()
            elif choice == "5":
                # Check if all necessary fields are filled
                if host and volume and password and output:
                    self.event_manager.trigger_event("process_data", {
                        "host": host,
                        "volume": volume,
                        "password": password,
                        "output": output,
                    })
                    break  # Exit the loop once data is processed
                else:
                    self.display_message("All fields must be filled before starting the processing. Please complete the inputs.", "error")
            elif choice == "6":
                self.display_message("Operation cancelled. Restarting data input process...", "info")
                return  # Restart the entire data input process by returning to the main menu
            else:
                self.display_message("Invalid selection. Please try again.", "info")

    def edit_config(self):
        """
        Allows the user to modify settings in the config file (config.json).
        Provides options to change the user interface, toggle verbose mode, and configure language settings.
        Displays the current status of each setting.
        """
        while True:
            # Load current configuration using the get_config method
            config = self.engine.load_config()  # Here, we call get_config to retrieve the configuration

            # Determine the status of the configurations
            gui_status = "[active]" if config.get("gui", False) else "[inactive]"
            verbose_status = "[active]" if config.get("verbose", False) else "[inactive]"
            check_status = "[active]" if config.get("check", False) else "[inactive]"

            print("\n")
            print("Settings")
            print("-" * 50)

            # Formatted output of options with status side by side
            print(f"{'Option':<40} {'Status'}")
            print("-" * 50)
            
            print(f"{'1: Toggle Graphical User Interface':<40} {gui_status}")
            print(f"{'2: Toggle verbose mode':<40} {verbose_status}")
            print(f"{'3: Toggle auto-tchunt-check':<40} {check_status}")
            print()
            print(f"'4: Return to Main Menu'")
            
            print("\n")

            choice = input("Please choose an option: ").strip()

            if choice == "1":
            # Confirm change and restart
                print("\033[38;5;214m\nChanging the user interface will restart the program immediately.\033[0m")
                confirm = input("Do you want to continue? (y/n): ").strip().lower()

                if confirm == "y":
                    # Trigger the event to change the user interface
                    self.event_manager.trigger_event("change_ui", None)
                    self.display_message("The program will now restart...", "info")
                    return
                else:
                    self.display_message("UI change canceled. Returning to the settings menu...", "info")
                    continue 
            elif choice == "2":
                # Trigger the event to toggle verbose mode
                self.event_manager.trigger_event("change_verbose", None)
            elif choice == "3":
                # Trigger event to change auto-check
                self.event_manager.trigger_event("change_check", None)
            elif choice == "4":
                return  # Return to the main menu without reprinting the title
            else:
                print("Invalid selection. Please try again.")


    def trigger_list_data(self):
        """
        Triggers the 'list_data' event to list available data.
        """
        self.event_manager.trigger_event("list_data", None)

    def display_message(self, message, message_type):
        config = self.engine.load_config()
        verbose = config.get("verbose", False)

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
            if verbose:
                print(f"{color}[VERBOSE] {message}{colors['reset']}")
        elif message_type == "error":
            print(f"{color}[ERROR] {message}{colors['reset']}")
        elif message_type == "message":
            print(f"{color}{message}{colors['reset']}")
        else:
            print(f"{color}[UNKNOWN] {message}{colors['reset']}")

    def show_documentation_menu(self):
        """
        Displays the documentation menu where the user can choose between different documentation options.
        """
        while True:
            print("\nDocumentation Menu")
            print("------------------------------------------")
            print("1: Show How-To Instructions")
            print("2: Show License Information")
            print("3: Show About Information")
            print("4: Return to Main Menu")
            print("\n")
            
            doc_choice = input("Please choose an option: ").strip()

            if doc_choice == "1":
                self.show_howto()  # Display How-To instructions
            elif doc_choice == "2":
                self.show_license()  # Display License information
            elif doc_choice == "3":
                self.show_about()  # Display About information
            elif doc_choice == "4":
                break  # Return to the main menu
            else:
                print("Invalid selection. Please try again.")


    def display_file(self, resource_path):
        """
        This method reads a Markdown file from the package resources and displays the content formatted on the console.
        :param resource_path: The path to the file to be displayed (relative to the package)
        """
        try:
            # Zugriff auf die Datei im Paket
            with importlib.resources.path("buttertoast.doc", resource_path) as file_path:
                with open(file_path, 'r') as file:
                    md_content = file.read()

            # Markdown-Inhalt rendern und anzeigen
            markdown = Markdown(md_content)
            self.console.print(markdown, width=80)

        except FileNotFoundError:
            print(f"Error: The file at {resource_path} could not be found.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def show_howto(self):
        """
        Menu for displaying the instructions.
        """
        self.display_file('howto.md')


    def show_license(self):
        """
        Menu for displaying the license.
        """
        self.display_file('LICENSE')


    def show_about(self):
        """
        Menu for displaying the about information.
        """
        self.display_file('about.md')


