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


class EventManager:
    def __init__(self):
        """
        Initialisiert den Event-Manager mit einer leeren Liste von Event-Handlern.
        """
        self.events = {}  # Dictionary für Event-Handler

    def register_event(self, event_name, handler):
        """
        Registriert einen Handler für ein bestimmtes Event.

        Args:
            event_name (str): Name des Events.
            handler (callable): Funktion oder Methode, die aufgerufen wird, wenn das Event ausgelöst wird.
        """
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(handler)

    def trigger_event(self, event_name, data=None):
        """
        Löst ein Event aus und ruft alle registrierten Handler auf.

        Args:
            event_name (str): Name des Events.
            data (optional): Daten, die an die Handler übergeben werden.
        """
        if event_name in self.events:
            for handler in self.events[event_name]:
                handler(data)
        else:
            print(f"[WARNUNG] Kein Handler für Event '{event_name}' registriert.")
