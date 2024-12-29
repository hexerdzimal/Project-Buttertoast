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

