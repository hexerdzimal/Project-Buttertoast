from abc import ABC, abstractmethod

class ModuleInterface(ABC):
    @abstractmethod
    def run(self):
        """Execute the main functionality of the module."""
        pass