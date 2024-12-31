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

class plugin_Interface(ABC):
    """
    Abstract base class for plugins. Defines the required interface methods
    that all plugin implementations must provide.
    """

    @abstractmethod
    def run(self):
        """
        Abstract method to execute the main functionality of the plugin.
        Must be implemented by any subclass.
        """
        pass
    #planned but not implemented yet:    
    #@abstractmethod
    #def info(self):
        """
        Abstract method to provide information about the plugin.
        Should be implemented by subclasses to return plugin-specific details.
        """
     #   pass