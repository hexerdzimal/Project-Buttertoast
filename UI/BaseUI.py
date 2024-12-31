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
    Eine abstrakte Basis für alle UI-Klassen. Beide UI-Typen (GUI und TUI) werden von dieser Klasse erben.
    """

    def __init__(self, event_manager):
        """
        Initialisiert die UI und verbindet sie mit dem Event-Manager.

        Args:
            event_manager (EventManager): Der Event-Manager für die Kommunikation.
        """
        self.event_manager = event_manager

    @abstractmethod
    def run(self):
        """
        Startet die UI-Schleife und wartet auf Benutzereingaben.
        """
        pass

    @abstractmethod
    def display_message(self, message, message_type):
        """
        Zeigt eine Nachricht basierend auf ihrem Typ an.
        
        Args:
            message (str): Die anzuzeigende Nachricht.
            message_type (str): Typ der Nachricht (z.B. "info", "verbose", "error").
        """
        pass

    @abstractmethod
    def edit_config():
        """
        Menü zum Bearbeiten der Einstellungen in der Config

        """

