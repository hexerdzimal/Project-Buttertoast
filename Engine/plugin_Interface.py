from abc import ABC, abstractmethod

class plugin_Interface(ABC):
    @abstractmethod
    def run(self):
        pass