from abc import ABC, abstractmethod

class plugin_interface(ABC):
    @abstractmethod
    def run(self):
        pass