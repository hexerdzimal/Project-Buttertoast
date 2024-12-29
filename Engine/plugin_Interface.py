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