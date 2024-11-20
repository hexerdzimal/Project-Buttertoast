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
