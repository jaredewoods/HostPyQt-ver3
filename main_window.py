# main_window.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QFrame, QTextEdit
import sys

from serial_service.serial_model import SerialModel
from serial_service.serial_view import SerialView
from serial_service.serial_controller import SerialController
from tcp_service.tcp_model import TCPModel
from tcp_service.tcp_view import TCPView
from tcp_service.tcp_controller import TCPController
from macro_service.macro_model import MacroModel
from macro_service.macro_view import MacroView
from macro_service.macro_controller import MacroController
from status_view import StatusView
from command_service.command_model import CommandModel
from command_service.command_view import CommandView
from command_service.command_controller import CommandController

from signal_distributor import SignalDistributor
from flag_state_manager import FlagStateManager, FlagStateView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize SignalDistributor and FlagStateManager
        self.signal_distributor = SignalDistributor()
        self.flag_state_manager = FlagStateManager(self.signal_distributor)
        self.flag_state_manager.state_updated.connect(self.on_state_changed)

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
        self.serial_controller = SerialController(self.serial_model, self.serial_view, self.flag_state_manager)

        self.tcp_model = TCPModel()
        self.tcp_view = TCPView()
        self.tcp_controller = TCPController(self.tcp_model, self.tcp_view, self.flag_state_manager)

        self.macro_model = MacroModel()
        self.macro_view = MacroView()
        self.macro_controller = MacroController(self.macro_model, self.macro_view)

        # Initialize command_compiler_service
        self.command_model = CommandModel()
        self.command_view = CommandView("Preset 1", "Preset 2", "Preset 3", "Preset 4")
        self.command_controller = CommandController(self.command_model, self.command_view)

        # Initialize status_view
        self.status_view = StatusView()

        # Create QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.serial_view, "Serial")
        self.tab_widget.addTab(self.tcp_view, "TCP / IP")
        self.tab_widget.addTab(self.macro_view, "Macro")

        # Adding to the Control layout
        self.control_layout.addWidget(self.tab_widget)
        self.control_layout.addWidget(self.command_view)
        self.control_layout.addWidget(self.status_view)

        # Adding to the main layout
        main_layout.addWidget(self.control_frame)
        main_layout.addWidget(self.log_display_frame)

        self.setWindowTitle("Main Window")

        # Open FlagStateView at startup
        self.flag_state_view = FlagStateView(self.flag_state_manager)
        self.flag_state_view.show()

    def on_state_changed(self, flag_name, value, update_condition):
        # Log all state changes
        self.log_display.append(f"State changed: {flag_name} -> {value}")

        # Handle specific state changes locally
        if flag_name == 'serial_connected':
            self.handle_serial_connected(value)
        elif flag_name == 'tcp_connected':
            self.handle_tcp_connected(value)

    def handle_serial_connected(self, value):
        self.log_display.append(f"Serial connection status: {value}")
        self.serial_controller.update_connection_state(value)

    def handle_tcp_connected(self, value):
        self.log_display.append(f"TCP connection status: {value}")
        self.tcp_controller.update_connection_state(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
