from UI.testMasterUI import BaseUI

from UI.testMasterUI import BaseUI

class TUI(BaseUI):
    def __init__(self, event_manager):
        """
        Initialize the TUI (Text User Interface) with an event manager.
        
        Args:
            event_manager: The event manager responsible for triggering events in the application.
        """
        super().__init__(event_manager)

    def display_title(self):
        """
        Displays the title of the application only once.
        This method is called at the start of the application to display the logo and version.
        """
        print(r"""
            +===================================================================================================+
            |                                                                         Version: 0.3 (cold) 2024  |
            |   ██████╗ ██╗   ██╗████████╗████████╗███████╗██████╗ ████████╗ ██████╗  █████╗ ███████╗████████╗  |
            |   ██╔══██╗██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝  |
            |   ██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝   ██║   ██║   ██║███████║███████╗   ██║     |
            |   ██╔══██╗██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗   ██║   ██║   ██║██╔══██║╚════██║   ██║     |
            |   ██████╔╝╚██████╔╝   ██║      ██║   ███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║███████║   ██║     |
            |   ╚═════╝  ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝     |
            |                                   The melting pot for polyglot.                                   |
            +===================================================================================================+
                                            by Fabian Kozlowski, Stefan Leippe, Malte Muthesius, Matthias Ferstl
                """)

    def run(self):
        """
        Displays the main menu and allows the user to choose actions like starting data input, listing plugins, or adjusting settings.
        This method also handles user navigation in the menu.
        """
        self.display_title()  # Display the title once at the start

        while True:
            print("\n")
            print("Main Menu")
            print("------------------------------------------")
            print("1: Start data input and processing")
            print("2: List plugins")
            print("3: Settings")
            print("4: Exit")
            print("\n")

            choice = input("Please choose an option: ").strip()

            if choice == "1":
                self.data_input_menu()  # Navigate to data input menu
            elif choice == "2":
                self.trigger_list_data()  # Trigger the list data event
            elif choice == "3":
                self.edit_config()  # Navigate to the settings menu
            elif choice == "4":
                print("Goodbye!")
                break  # Exit the application
            else:
                print("Invalid selection. Please try again.")

    def data_input_menu(self):
        """
        Guides the user through the data input process where they first provide all necessary information (host, volume, 
        password, and output file path), and then allows them to modify specific fields or trigger the 'process_data' event.
        """
        # Step 1: Directly ask for all required fields
        print("\nEnter the required file paths and password.")
        host = input("Host file path: ").strip()
        volume = input("Volume file path: ").strip()
        password = input("Password: ").strip()
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
                    print("All fields must be filled before starting the processing. Please complete the inputs.")
            elif choice == "6":
                print("Operation cancelled. Restarting data input process...")
                return  # Restart the entire data input process by returning to the main menu
            else:
                print("Invalid selection. Please try again.")

    def edit_config(self):
        """
        Allows the user to modify settings in the config file (config.json).
        Provides options to change the user interface, toggle verbose mode, and configure language settings.
        """
        print("\n")
        print("Settings")
        print("------------------------------------------")
        print("1: Change User Interface")
        print("2: Toggle verbose mode")
        print("3: Language settings")
        print("4: Return to Main Menu")
        print("\n")

        choice = input("Please choose an option: ").strip()

        if choice == "1":
            # Trigger the event to change the user interface
            self.event_manager.trigger_event("change_ui", None)
        elif choice == "2":
            # Trigger the event to toggle verbose mode
            self.event_manager.trigger_event("change_verbose", None)
        elif choice == "3":
            # Language settings are not implemented yet
            print("Language settings are not implemented.")
        elif choice == "4":
            return  # Return to the main menu without reprinting the title
        else:
            print("Invalid selection. Please try again.")

    def trigger_change_language(self):
        """
        Triggers the 'change_language' event to update language settings.
        """
        print("\n--- Listing data ---")
        self.event_manager.trigger_event("change_language", None)

    def trigger_change_ui(self):
        """
        Triggers the 'change_ui' event to update the user interface settings.
        """
        print("\n--- Listing data ---")
        self.event_manager.trigger_event("change_ui", None)

    def trigger_change_verbose(self):
        """
        Triggers the 'change_verbose' event to toggle verbose mode settings.
        """
        print("\n--- Listing data ---")
        self.event_manager.trigger_event("change_verbose", None)

    def trigger_list_data(self):
        """
        Triggers the 'list_data' event to list available data.
        """
        print("\n")
        print("--- Listing data ---")
        self.event_manager.trigger_event("list_data", None)

    def display_message(self, message, message_type):
        if message_type == "info":
            print(f"[INFO] {message}")
        elif message_type == "verbose":
            print(f"[VERBOSE] {message}")
        elif message_type == "error":
            print(f"[ERROR] {message}")
        elif message_type == "message":
            print(f"{message}")
        else:
            print(f"{message}")
