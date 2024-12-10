from UI.testMasterUI import BaseUI
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QMessageBox, QLineEdit, QFileDialog, QHBoxLayout, QTextEdit, QCheckBox
)
import sys



class FileButton(QPushButton):
    """Eine benutzerdefinierte Schaltfläche, die Drag-and-Drop unterstützt."""
    def __init__(self, label, parent=None, drop_handler=None):
        super().__init__(label, parent)
        self.setAcceptDrops(True)
        self.drop_handler = drop_handler  # Callback-Funktion zur Verarbeitung der Datei

    def dragEnterEvent(self, event):
        """Wenn eine Datei gezogen wird, erlauben, dass sie fallen gelassen wird."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Verarbeite die Datei, wenn sie abgelegt wird."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.drop_handler:  # Wenn ein Handler definiert ist
                self.drop_handler(file_path)

class GUI(BaseUI):
    def __init__(self, event_manager):
        super().__init__(event_manager)

        # Attribute für Datei- und Speicherorte
        self.host_file = None
        self.guest_file = None
        self.save_location = None

        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        # Hauptfenster erstellen
        self.window = QMainWindow()
        self.window.setWindowTitle("Buttertoast")
        self.window.setGeometry(100, 100, 600, 600)

        # Zentrales Widget erstellen
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        self.window.setWindowIcon(QIcon("res/BuToTransp.png"))

        # Hintergrundbild hinzufügen
        self.background_label = QLabel(central_widget)
        self.background_label.setPixmap(QPixmap("res/BuToTransp.png"))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 600, 600)

        # Hauptlayout (vertikal)
        main_layout = QVBoxLayout(central_widget)

        # Container für die Datei-Buttons (Host, Guest, Speicherort)
        file_buttons_layout = QHBoxLayout()

        self.host_button = FileButton("Host-Datei auswählen", central_widget, 
                                      drop_handler=lambda path: self.handle_dropped_file("Host", path))
        self.guest_button = FileButton("Guest-Datei auswählen", central_widget, 
                                       drop_handler=lambda path: self.handle_dropped_file("Guest", path))
        self.save_button = QPushButton("Speicherort auswählen", central_widget)

        # Button-Aktionen
        self.host_button.clicked.connect(lambda: self.open_file("Host"))
        self.guest_button.clicked.connect(lambda: self.open_file("Guest"))
        self.save_button.clicked.connect(self.save_file)

        file_buttons_layout.addWidget(self.host_button)
        file_buttons_layout.addWidget(self.guest_button)
        file_buttons_layout.addWidget(self.save_button)

        # Fixiere die Datei-Buttons ganz oben
        file_buttons_container = QWidget()
        file_buttons_container.setLayout(file_buttons_layout)
        central_widget.layout().addWidget(file_buttons_container)

        # Passwortfeld
        self.password_entry = QLineEdit(central_widget)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Passwort eingeben")
        self.password_entry.textChanged.connect(self.update_execute_button_state)

        self.show_password_checkbox = QCheckBox("Passwort anzeigen", central_widget)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password)

        # Ausführen und Abbrechen Buttons
        self.execute_button = QPushButton("Ausführen", central_widget)
        self.execute_button.setEnabled(False)  # Initial deaktiviert
        self.cancel_button = QPushButton("Abbrechen", central_widget)
        self.execute_button.clicked.connect(self.on_execute_click)
        self.cancel_button.clicked.connect(self.on_exit_click)

        # Log-Ausgabe
        self.log_output = QTextEdit(central_widget)
        self.log_output.setReadOnly(True)

        # Log-Toggle-Button
        self.toggle_log_button = QPushButton("Log anzeigen", central_widget)
        self.toggle_log_button.setCheckable(True)
        self.toggle_log_button.clicked.connect(self.toggle_log_window)

        # Animation für Log
        self.animation = QPropertyAnimation(self.log_output, b"maximumHeight")
        self.animation.setDuration(300)

        # Layout-Organisation
        # Datei-Auswahl-Buttons
        file_buttons_layout = QHBoxLayout()
        file_buttons_layout.addWidget(self.host_button)
        file_buttons_layout.addWidget(self.guest_button)
        file_buttons_layout.addWidget(self.save_button)

        # Passwortfeld und Checkbox
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_entry)
        password_layout.addWidget(self.show_password_checkbox)

        # Ausführen und Abbrechen-Buttons nebeneinander
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addWidget(self.execute_button)
        action_buttons_layout.addWidget(self.cancel_button)

        # Log-Bereich
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.log_output)
        bottom_layout.addWidget(self.toggle_log_button)

        # Alles zusammenfügen
        main_layout.addLayout(file_buttons_layout)  # Datei-Auswahl-Buttons im Hauptlayout
        main_layout.addLayout(password_layout)      # Passwortfeld und Checkbox
        main_layout.addLayout(action_buttons_layout)  # Ausführen und Abbrechen
        main_layout.addLayout(bottom_layout)        # Log-Bereich

        # Fenster anzeigen
        self.center_window()
        self.window.show()

        # Log-Bereich zu Beginn ausblenden
        self.log_output.setMaximumHeight(0)
        self.toggle_log_button.setChecked(False)

    def handle_dropped_file(self, file_type, file_path):
        """Verarbeitet die abgeworfene Datei je nach Dateityp."""
        if file_type == "Host":
            self.host_file = file_path
            self.host_button.setText("Host-Datei ausgewählt ✔")
            self.log_output.append(f"Host-Datei ausgewählt: {file_path}")
        elif file_type == "Guest":
            self.guest_file = file_path
            self.guest_button.setText("Guest-Datei ausgewählt ✔")
            self.log_output.append(f"Guest-Datei ausgewählt: {file_path}")

        self.update_execute_button_state()

    def update_execute_button_state(self):
        """Aktiviert oder deaktiviert den Ausführen-Button basierend auf den Eingaben."""
        if self.host_file and self.guest_file and self.save_location and self.password_entry.text().strip():
            self.execute_button.setEnabled(True)
        else:
            self.execute_button.setEnabled(False)

    def toggle_password(self):
        """Zeigt oder versteckt das Passwort."""
        if self.show_password_checkbox.isChecked():
            self.password_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)

    def open_file(self, file_type):
        """Öffnet einen Datei-Selektor."""
        file_dialog = QFileDialog(self.window)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.handle_dropped_file(file_type, selected_file)

    def save_file(self):
        """Speicherort auswählen."""
        save_dialog = QFileDialog(self.window)
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if save_dialog.exec():
            save_path = save_dialog.selectedFiles()[0]
            self.save_location = save_path
            self.save_button.setText("Speicherort ausgewählt ✔")  # Häkchen hinzufügen
            self.log_output.append(f"Speicherort ausgewählt: {save_path}")
            self.update_execute_button_state()

    def on_execute_click(self):
        """Führt die Hauptlogik aus."""
        host = self.host_file
        guest = self.guest_file
        password = self.password_entry.text()
        saveloc = self.save_location
        
        # self.event_manager.handle_user_input(host, guest, password, saveloc)
        self.event_manager.trigger_event("process_data", {
            "host": host,
            "volume": guest,
            "password": password,
            "output": saveloc,
        })
        # Engine.handle_user_input(host, guest, password, saveloc)
        
        self.log_output.append("Ausführung gestartet...")

    def on_exit_click(self):
        """Schließt das Programm."""
        reply = QMessageBox.question(self.window, "Beenden", "Möchten Sie das Programm wirklich beenden?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.app.quit()

    def toggle_log_window(self):
        """Ein- oder Ausklappen des Log-Bereichs."""
        if self.toggle_log_button.isChecked():
            self.toggle_log_button.setText("Log ausblenden")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(150)  # Höhe für sichtbaren Log-Bereich
        else:
            self.toggle_log_button.setText("Log anzeigen")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(0)  # Log-Bereich ausblenden
        self.animation.start()

    def center_window(self):
        """Zentriert das Fenster auf dem Bildschirm."""
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.window.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.window.move(window_geometry.topLeft())

    
    def display_message(self, message, message_type):
        """Zeigt eine Nachricht im Log-Bereich der GUI an."""
        if message_type == "info":
            self.log_output.append(f"[INFO] {message}")
        elif message_type == "verbose":
            self.log_output.append(f"[VERBOSE] {message}")
        elif message_type == "error":
            self.log_output.append(f"[ERROR] {message}")
        elif message_type == "message":
            self.log_output.append(f"{message}")
        else:
            self.log_output.append(f"[UNKNOWN] {message}")
        
    
    def edit_config():
        pass



    def run(self):
        """Startet die GUI."""
        self.app.exec()
