from UI.testMasterUI import BaseUI
from PySide6.QtCore import QPropertyAnimation, Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QMessageBox, QLineEdit, QFileDialog, QHBoxLayout, QTextEdit, QCheckBox
)
import sys

class FileButton(QPushButton):
    """A custom button that supports drag-and-drop functionality."""
    def __init__(self, label, parent=None, drop_handler=None):
        super().__init__(label, parent)
        self.setAcceptDrops(True)
        self.drop_handler = drop_handler  # Callback function to process the dropped file

    def dragEnterEvent(self, event):
        """Allow files to be dropped when dragged into the button."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Process the file when it is dropped."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if self.drop_handler: # If a handler is defined
                self.drop_handler(file_path)

class GUI(BaseUI):
    def __init__(self, event_manager):
        super().__init__(event_manager)

        # Attributes for files and save locations
        self.host_file = None
        self.guest_file = None
        self.save_location = None

        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle("Buttertoast")
        self.window.setGeometry(100, 100, 600, 600)

        # Create central widget
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        self.window.setWindowIcon(QIcon("res/BuToTransp.png"))

        # Add background image
        self.background_label = QLabel(central_widget)
        self.background_label.setPixmap(QPixmap("res/BuToTransp.png"))
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 600, 600)

        # Main layout (vertical)
        main_layout = QVBoxLayout(central_widget)

        # Container for file buttons (Host, Guest, Save Location)
        file_buttons_layout = QHBoxLayout()

        self.host_button = FileButton("Select Host File", central_widget, 
                                      drop_handler=lambda path: self.handle_dropped_file("Host", path))
        self.guest_button = FileButton("Select Guest File", central_widget, 
                                       drop_handler=lambda path: self.handle_dropped_file("Guest", path))
        self.save_button = QPushButton("Select Save Location", central_widget)

        # Button actions
        self.host_button.clicked.connect(lambda: self.open_file("Host"))
        self.guest_button.clicked.connect(lambda: self.open_file("Guest"))
        self.save_button.clicked.connect(self.save_file)

        file_buttons_layout.addWidget(self.host_button)
        file_buttons_layout.addWidget(self.guest_button)
        file_buttons_layout.addWidget(self.save_button)

        # Fix the file buttons at the top
        file_buttons_container = QWidget()
        file_buttons_container.setLayout(file_buttons_layout)
        central_widget.layout().addWidget(file_buttons_container)

        # Password field
        self.password_entry = QLineEdit(central_widget)
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setPlaceholderText("Enter Password")
        self.password_entry.textChanged.connect(self.update_execute_button_state)

        self.show_password_checkbox = QCheckBox("Show Password", central_widget)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password)

        # Execute and Cancel buttons
        self.execute_button = QPushButton("Execute", central_widget)
        self.execute_button.setEnabled(False)  # Initially disabled
        self.cancel_button = QPushButton("Cancel", central_widget)
        self.execute_button.clicked.connect(self.on_execute_click)
        self.cancel_button.clicked.connect(self.on_exit_click)

        # Log output
        self.log_output = QTextEdit(central_widget)
        self.log_output.setReadOnly(True)

        # Log toggle button
        self.toggle_log_button = QPushButton("Show Log", central_widget)
        self.toggle_log_button.setCheckable(True)
        self.toggle_log_button.clicked.connect(self.toggle_log_window)

        # Animation for log
        self.animation = QPropertyAnimation(self.log_output, b"maximumHeight")
        self.animation.setDuration(300)

        # Layouts
        # File selection buttons
        file_buttons_layout = QHBoxLayout()
        file_buttons_layout.addWidget(self.host_button)
        file_buttons_layout.addWidget(self.guest_button)
        file_buttons_layout.addWidget(self.save_button)

        # Password field and checkbox
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_entry)
        password_layout.addWidget(self.show_password_checkbox)

        # Execute and Cancel buttons side by side
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addWidget(self.execute_button)
        action_buttons_layout.addWidget(self.cancel_button)

        # Log area
        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.log_output)
        bottom_layout.addWidget(self.toggle_log_button)

        # Combine everything
        main_layout.addLayout(file_buttons_layout) # File selection buttons in main layout
        main_layout.addLayout(password_layout) # Password field and checkbox
        main_layout.addLayout(action_buttons_layout) # Execute and Cancel
        main_layout.addLayout(bottom_layout) # Log area

        # Show window
        self.center_window()
        self.window.show()

        # Hide log area initially
        self.log_output.setMaximumHeight(0)
        self.toggle_log_button.setChecked(False)

    def handle_dropped_file(self, file_type, file_path):
        """Processes the dropped file based on its type."""
        if file_type == "Host":
            self.host_file = file_path
            self.host_button.setText("Host File Selected ✔")
            self.log_output.append(f"Host file selected: {file_path}")
        elif file_type == "Guest":
            self.guest_file = file_path
            self.guest_button.setText("Guest File Selected ✔")
            self.log_output.append(f"Guest file selected: {file_path}")

        self.update_execute_button_state()

    def update_execute_button_state(self):
        """Enables or disables the Execute button based on input fields."""
        if self.host_file and self.guest_file and self.save_location and self.password_entry.text().strip():
            self.execute_button.setEnabled(True)
        else:
            self.execute_button.setEnabled(False)

    def toggle_password(self):
        """Shows or hides the password."""
        if self.show_password_checkbox.isChecked():
            self.password_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)

    def open_file(self, file_type):
        """Opens a file selector dialog."""
        file_dialog = QFileDialog(self.window)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.handle_dropped_file(file_type, selected_file)

    def save_file(self):
        """Selects a save location."""
        save_dialog = QFileDialog(self.window)
        save_dialog.setAcceptMode(QFileDialog.AcceptSave)
        if save_dialog.exec():
            save_path = save_dialog.selectedFiles()[0]
            self.save_location = save_path
            self.save_button.setText("Save Location Selected ✔")  # Add checkmark
            self.log_output.append(f"Save location selected: {save_path}")
            self.update_execute_button_state()

    def on_execute_click(self):
        """Executes the main logic."""
        host = self.host_file
        guest = self.guest_file
        password = self.password_entry.text()
        saveloc = self.save_location
        
        self.event_manager.trigger_event("process_data", {
            "host": host,
            "volume": guest,
            "password": password,
            "output": saveloc,
        })
        
        self.log_output.append("Execution started...")

    def on_exit_click(self):
        """Closes the program."""
        reply = QMessageBox.question(self.window, "Exit", "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.app.quit()

    def toggle_log_window(self):
        """Expands or collapses the log area."""
        if self.toggle_log_button.isChecked():
            self.toggle_log_button.setText("Hide Log")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(150)  # Height for visible log area
        else:
            self.toggle_log_button.setText("Show Log")
            self.animation.setStartValue(self.log_output.maximumHeight())
            self.animation.setEndValue(0)  # Collapse log area
        self.animation.start()

    def center_window(self):
        """Centers the window on the screen."""
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.window.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.window.move(window_geometry.topLeft())

    def display_message(self, message, message_type):
        """Displays a message in the log area of the GUI."""
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
        """Starts the GUI."""
        self.app.exec()
