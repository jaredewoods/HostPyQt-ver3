# main_window.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QFrame, QTextEdit
import sys

from serial_service.serial_model import SerialModel
from serial_service.serial_view import SerialView
from serial_service.serial_controller import SerialController
from tcp_service.tcp_view import TCPView
from macro_service.macro_view import MacroView
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

        # Control Frame and layout
        self.control_frame = QFrame()
        self.control_layout = QVBoxLayout(self.control_frame)

        # Log display frame
        self.log_display_frame = QFrame()
        self.log_display_layout = QVBoxLayout(self.log_display_frame)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFixedWidth(350)
        self.log_display_layout.addWidget(self.log_display)

        # Initialize MVC components
        self.serial_model = SerialModel()
        self.serial_view = SerialView()
        self.serial_controller = SerialController(self.serial_model, self.serial_view)
        self.tcp_view = TCPView()
        self.macro_view = MacroView()

        # Initialize custom_command_service
        self.custom_command_model = CustomCommandModel()
        self.custom_command_view = CustomCommandView("Preset 1", "Preset 2", "Preset 3", "Preset 4")
        self.custom_command_controller = CustomCommandController(self.custom_command_model, self.custom_command_view)

        # Initialize status_view
        self.status_view = StatusView()

        # Create QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.serial_view, "Serial")
        self.tab_widget.addTab(self.tcp_view, "TCP/IP")
        self.tab_widget.addTab(self.macro_view, "Macro")

        # Adding to the Control layout
        self.control_layout.addWidget(self.tab_widget)
        self.control_layout.addWidget(self.custom_command_view)
        self.control_layout.addWidget(self.status_view)

        # Adding to the main layout
        main_layout.addWidget(self.control_frame)
        main_layout.addWidget(self.log_display_frame)

        self.setWindowTitle("Main Window")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
