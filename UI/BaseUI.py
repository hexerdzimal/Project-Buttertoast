from tkinter import filedialog

class BaseUI:
    def __init__(self):
        self.controller = None  # Referenz auf die Engine

    def openFile(self, file_type):
        return filedialog.askopenfilename(title=f"{file_type}-Datei auswählen")

    def saveFile(self):
        return filedialog.asksaveasfilename(title="Speicherort auswählen")

    def enterPassword(self, password=None):
        return password if password else "buttertoast"

    def startProcessing(self, host, volume, password, output):
        print(f"Host: {host}, Volume: {volume}, Passwort: {password}, Ausgabe: {output}")
        return (volume, host, output, password)

    def set_controller(self, controller):
        """
        Verknüpft die UI mit einem Controller (der Engine).
        :param controller: Instanz der Engine
        """
        self.controller = controller

    def show_result(self, result):
        """
        Zeigt das Ergebnis der Verarbeitung an. 
        Muss in abgeleiteten Klassen implementiert werden.
        :param result: Ergebnisdaten
        """
        raise NotImplementedError("Die 'show_result' Methode muss in der abgeleiteten Klasse implementiert werden.")

    def show_error(self, message):
        """
        Zeigt eine Fehlermeldung an. 
        Muss in abgeleiteten Klassen implementiert werden.
        :param message: Fehlermeldung
        """
        raise NotImplementedError("Die 'show_error' Methode muss in der abgeleiteten Klasse implementiert werden.")

    def run(self):
        """
        Startet die UI. 
        Muss in abgeleiteten Klassen implementiert werden.
        """
        raise NotImplementedError("Die 'run' Methode muss in der abgeleiteten Klasse implementiert werden.")

    def collect_user_input(self):
        """
        Sammelt Benutzereingaben und übergibt sie an den Controller.
        Muss in abgeleiteten Klassen implementiert werden.
        """
        raise NotImplementedError("Die 'collect_user_input' Methode muss in der abgeleiteten Klasse implementiert werden.")
    
    def exit(self):
        print("Beenden")
        exit()