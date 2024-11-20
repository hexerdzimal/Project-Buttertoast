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
    def show_result(self, result):
        """
        Zeigt das Ergebnis der Datenverarbeitung an.

        Args:
            result (dict): Das Ergebnis der Verarbeitung.
        """
        pass

    @abstractmethod
    def show_error(self, message):
        """
        Zeigt eine Fehlermeldung an.

        Args:
            message (str): Die Fehlermeldung.
        """
        pass
