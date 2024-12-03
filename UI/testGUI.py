from UI.testMasterUI import BaseUI
from PySide6.QtCore import QPropertyAnimation, QSize, Qt 
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout,
    QVBoxLayout, QWidget, QMessageBox, QLineEdit, QSplitter, QTextEdit, QFileDialog
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
        self.window.setWindowTitle("GUI mit Drag and Drop und Button")
        self.window.setGeometry(100, 100, 700, 400)

        # Zentrales Widget erstellen
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)

        # Hauptlayout (vertikal) erstellen
        main_layout = QVBoxLayout()

        # Drei horizontale Abschnitte (Labels als Platzhalter)
        top_widget = QWidget()  # Für die horizontale Anordnung der drei vertikalen Layouts
        middle_label = QLabel("Mittlerer Bereich")
        bottom_label = QLabel("Unterer Bereich")

        # Horizontales Layout für die mittlere Aufteilung
        top_layout = QHBoxLayout()

        # Drei vertikale Layouts in der Mitte hinzufügen
        left_layout = QVBoxLayout()
        center_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Labels für die vertikalen Layouts
        left_label = QLabel("Linker Bereich")
        center_label = QLabel("Mittlerer Bereich")
        right_label = QLabel("Rechter Bereich")

        left_layout.addWidget(left_label, alignment=Qt.AlignTop)
        center_layout.addWidget(center_label, alignment=Qt.AlignTop)
        right_layout.addWidget(right_label, alignment=Qt.AlignTop)

        # Drag and Drop und Button für den linken Bereich
        self.left_drop_area, self.left_file_path_label = self.create_drag_and_drop_button(is_left=True)

        # Drag and Drop und Button für den rechten Bereich
        self.right_drop_area, self.right_file_path_label = self.create_drag_and_drop_button(is_left=False)

        # Hinzufügen von Drop-Bereich und Button zum linken Layout
        left_layout.addWidget(self.left_drop_area)
        left_layout.addWidget(self.left_file_path_label)  # Label für den Dateipfad

        # Hinzufügen von Drop-Bereich und Button zum rechten Layout
        right_layout.addWidget(self.right_drop_area)
        right_layout.addWidget(self.right_file_path_label)  # Label für den Dateipfad

        # Vertikale Layouts ins horizontale Layout einfügen
        top_layout.addLayout(left_layout)
        top_layout.addLayout(center_layout)
        top_layout.addLayout(right_layout)

        # Mittleres Widget mit dem horizontalen Layout verknüpfen
        top_widget.setLayout(top_layout)

        # Bereiche zum Hauptlayout hinzufügen
        main_layout.addWidget(top_widget)
        main_layout.addWidget(middle_label)

        # Log-Ausgabe (dies ist eine Beispielausgabe, kannst es anpassen)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlainText("Log-Ausgabe wird hier angezeigt...")

        # Button zum Ein- und Ausklappen des Log-Fensters
        self.toggle_log_button = QPushButton("Log anzeigen", self.window)
        self.toggle_log_button.setCheckable(True)
        self.toggle_log_button.clicked.connect(self.toggle_log_window)

        # Layout für den Log-Bereich (unten)
        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log_output)
        log_layout.addWidget(self.toggle_log_button)

        # Log-Bereich in den unteren Bereich (bottom_label) hinzufügen
        bottom_widget = QWidget()
        bottom_widget.setLayout(log_layout)
        main_layout.addWidget(bottom_widget)

        # Hauptlayout dem zentralen Widget zuweisen
        central_widget.setLayout(main_layout)

        # Fenster anzeigen
        self.window.show()

        # Animation für Log-Ausgabe
        self.animation = QPropertyAnimation(self.log_output, b"maximumHeight")
        self.animation.setDuration(300)  # Animation dauert 300ms

    def create_drag_and_drop_button(self, is_left=True):
        """Erstellt einen Drag-and-Drop-Bereich, der auf Klick öffnet, und zeigt den Dateipfad an."""
        # Drag-and-Drop Bereich
        drop_area = QWidget()
        drop_area.setAcceptDrops(True)  # Aktiviert Drag-and-Drop für dieses Widget

        # Stylesheet für den Drag-and-Drop Bereich: Hintergrundfarbe und Hover-Effekt
        drop_area.setStyleSheet("""
            QWidget {
                border: 1px dashed black;
                border-radius: 10px;
            }
            QWidget:hover {
                background-color: #808080;  /* Helleres Blau, wenn über dem Bereich */
            }
        """)

        drop_area.setFixedSize(200, 100)  # Feste Größe für den Drag-and-Drop Bereich

        # Label für den Drag-and-Drop Bereich
        drop_area_label = QLabel("Ziehen Sie eine Datei hierhin")
        drop_area_label.setAlignment(Qt.AlignCenter)

        # Layout für den Drop-Bereich mit dem Label hinzufügen
        drop_area_layout = QVBoxLayout()
        drop_area_layout.addWidget(drop_area_label)
        drop_area.setLayout(drop_area_layout)

        # Connect the drop area with the drag-and-drop events
        drop_area.dragEnterEvent = lambda event: self.dragEnterEvent(event, is_left)
        drop_area.dropEvent = lambda event: self.dropEvent(event, is_left)

        # Hier klicken auf den Bereich öffnet den Dateidialog
        drop_area.mousePressEvent = self.open_file_dialog_on_click

        # Label für den Dateipfad (wird später aktualisiert)
        file_path_label = QLabel("Kein Dateipfad ausgewählt")
        file_path_label.setAlignment(Qt.AlignCenter)

        return drop_area, file_path_label

    def open_file_dialog_on_click(self, event):
        """Öffnet den Dateidialog, wenn auf den Drag-and-Drop-Bereich geklickt wird."""
        # Öffnet den Dateidialog und aktualisiert den Dateipfad
        file_dialog = QFileDialog(self.window)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Alle Dateien (*.*)")
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                # Datei hinzugefügt, Pfad anzeigen
                self.update_file_path(selected_files[0], is_left=True)

    def dragEnterEvent(self, event, is_left=True):
        """Ermöglicht das Akzeptieren von Drag-and-Drop-Events."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event, is_left=True):
        """Verarbeitet die Datei, die per Drag-and-Drop abgelegt wurde."""
        urls = event.mimeData().urls()
        if urls:
            # Den Dateipfad extrahieren und weiterverarbeiten
            file_path = urls[0].toLocalFile()
            self.update_file_path(file_path, is_left)

    def update_file_path(self, file_path, is_left):
        """Aktualisiert das Label mit dem Dateipfad, abhängig vom Drop-Bereich."""
        if is_left:
            self.left_file_path_label.setText(f"Dateipfad: {file_path}")
        else:
            self.right_file_path_label.setText(f"Dateipfad: {file_path}")

    def toggle_log_window(self):
        """Ein- oder Ausklappen des Log-Bereichs."""
        if self.toggle_log_button.isChecked():
            self.toggle_log_button.setText("Log ausblenden")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(150)  # Höhe des ausgeklappten Log-Bereichs
        else:
            self.toggle_log_button.setText("Log anzeigen")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(0)  # Einklappen des Log-Bereichs
        self.animation.start()

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
