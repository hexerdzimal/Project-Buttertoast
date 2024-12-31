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
        Initializes the event manager with an empty list of event handlers.
        """
        self.events = {}  # Dictionary for event handlers

    def register_event(self, event_name, handler):
        """
        Registers a handler for a specific event.

        Args:
            event_name (str): Name of the event.
            handler (callable): Function or method to be called when the event is triggered.
        """
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(handler)

    def trigger_event(self, event_name, data=None):
        """
        Triggers an event and calls all registered handlers.

        Args:
            event_name (str): Name of the event.
            data (optional): Data to be passed to the handlers.
        """
        if event_name in self.events:
            for handler in self.events[event_name]:
                handler(data)
        else:
            print(f"[WARNING] No handler registered for event '{event_name}'.")



