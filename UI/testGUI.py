from UI.testMasterUI import BaseUI
from PySide6.QtCore import QPropertyAnimation, QSize, Qt 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QMessageBox, QLineEdit, QSplitter, QTextEdit
)
import sys

class GUI(BaseUI):
    def __init__(self, event_manager):
        super().__init__(event_manager)

        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        # Hauptfenster erstellen
        self.window = QMainWindow()
        self.window.setWindowTitle("GUI mit Log-Umschalter")
        self.window.setGeometry(100, 100, 500, 400)

        # GUI-Elemente erstellen (oben)
        self.label = QLabel("Willkommen zur erweiterten GUI!", self.window)
        self.label.setStyleSheet("font-size: 16px; color: #333; padding: 5px;")

        self.input_field = QLineEdit(self.window)
        self.input_field.setPlaceholderText("Gib hier etwas ein...")

        self.button = QPushButton("Klick mich", self.window)
        self.button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button.clicked.connect(self.on_button_click)

        # Log-Umschalter-Button
        self.toggle_log_button = QPushButton("Log anzeigen", self.window)
        self.toggle_log_button.setCheckable(True)
        self.toggle_log_button.clicked.connect(self.toggle_log_window)

        # Layout für oberen Teil definieren
        upper_layout = QVBoxLayout()
        upper_layout.addWidget(self.label)
        upper_layout.addWidget(self.input_field)
        upper_layout.addWidget(self.button)
        upper_layout.addWidget(self.toggle_log_button)
        
        upper_container = QWidget()
        upper_container.setLayout(upper_layout)

        # Log-Fenster (unten)
        self.log_output = QTextEdit(self.window)
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background-color: #f0f0f0;")
        self.log_output.setText("Log-Ausgaben werden hier angezeigt...\n")
        self.log_output.setMaximumHeight(0)  # Startet versteckt

        # Splitter für vertikale Aufteilung
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(upper_container)
        self.splitter.addWidget(self.log_output)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)

        # Animation vorbereiten
        self.animation = QPropertyAnimation(self.log_output, b"maximumHeight")
        self.animation.setDuration(300)  # 300 ms Dauer

        # Zentrales Widget setzen
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.splitter)
        container.setLayout(layout)
        self.window.setCentralWidget(container)

    def toggle_log_window(self):
        if self.toggle_log_button.isChecked():
            self.toggle_log_button.setText("Log ausblenden")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(150)  # Höhe des ausgeklappten Log-Bereichs
        else:
            self.toggle_log_button.setText("Log anzeigen")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(0)  # Einklappen des Log-Bereichs
        self.animation.start()

    def on_button_click(self):
        user_text = self.input_field.text()
        if user_text:
            self.display_message(f"Du hast eingegeben: {user_text}", "info")
            self.log_output.append(f"Eingabe: {user_text}")
        else:
            self.display_message("Das Eingabefeld ist leer!", "warning")
            self.log_output.append("Warnung: Leere Eingabe erkannt.")

    def on_button_click(self):
        self.display_message("Button wurde geklickt!", "info")

    def run(self):
        self.window.show()  # Hauptfenster anzeigen
        self.app.exec()     # Event-Schleife starten

    def display_message(self, message, message_type):
        if message_type == "info":
            QMessageBox.information(self.window, "Info", message)
        elif message_type == "error":
            QMessageBox.critical(self.window, "Fehler", message)
        else:
            QMessageBox.warning(self.window, "Nachricht", message)

    def edit_config(self):
        self.display_message("Config-Editor wird noch implementiert.", "info")