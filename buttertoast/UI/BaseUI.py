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


from abc import ABC, abstractmethod

class BaseUI(ABC):
    """
    An abstract base class for all UI classes. Both UI types (GUI and TUI) will inherit from this class.
    """

    def __init__(self, engine, event_manager):
        """
        Initializes the UI and connects it to the event manager.

        Args:
            event_manager (EventManager): The event manager for communication.
        """
        self.event_manager = event_manager
        self.engine = engine

    @abstractmethod
    def run(self, engine):
        """
        Starts the UI loop and waits for user input.
        """
        pass

    @abstractmethod
    def display_message(self, message, message_type):
        """
        Displays a message based on its type.
        
        Args:
            message (str): The message to be displayed.
            message_type (str): The type of the message (e.g., "info", "verbose", "error").
        """
        pass

    @abstractmethod
    def edit_config(self):
        """
        Menu for editing settings in the configuration.
        """
        pass

    @abstractmethod
    def show_howto(self):
        """
        Menu for displaying the instructions.
        """
        pass

    @abstractmethod
    def show_license(self):
        """
        Menu for displaying the license.
        """
        pass

    @abstractmethod
    def show_about(self):
        """
        Menu for displaying the about information.
        """
        pass
