# main_window.py
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QFrame, QTextEdit
import sys

from serial_tab import SerialView
from tcp_tab import TCPView
from macro_tab import MacroView
from status_view import StatusView
from custom_command_service.custom_command_model import CustomCommandModel
from custom_command_service.custom_command_view import CustomCommandView
from custom_command_service.custom_command_controller import CustomCommandController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left frame and layout
        self.control_frame = QFrame()
        self.control_layout = QVBoxLayout(self.control_frame)

        # QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(SerialView(), "Serial")
        self.tab_widget.addTab(TCPView(), "TCP/IP")
        self.tab_widget.addTab(MacroView(), "Macro")

        self.custom_command_view = CustomCommandView("Preset 1", "Preset 2", "Preset 3", "Preset 4")

        # Adding widgets to the left layout
        self.control_layout.addWidget(self.tab_widget)
        self.control_layout.addWidget(self.custom_command_view)

        # Initialize the Model
        self.custom_command_model = CustomCommandModel()

        # Initialize the Control
        self.custom_command_controller = CustomCommandController(self.custom_command_model, self.custom_command_view)

        # Initialize the Status View
        self.status_view = StatusView()

        # Log display frame
        self.log_display_frame = QFrame()
        self.log_display_layout = QVBoxLayout(self.log_display_frame)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFixedWidth(350)
        self.log_display_layout.addWidget(self.log_display)

        # Adding frames to the main layout
        main_layout.addWidget(self.control_frame)
        main_layout.addWidget(self.status_view)
        main_layout.addWidget(self.log_display_frame)

        self.setWindowTitle("Main Window")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
