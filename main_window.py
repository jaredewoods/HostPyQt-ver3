# main_window.py
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QFrame, QTextEdit
import sys

from serial_view import SerialView
from tcp_view import TCPView
from macro_view import MacroView
from preset_buttons_view import PresetButtonsView
from status_view import StatusView
from custom_command_view import CustomCommandView
from sequence_view import SequenceView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Left frame and layout
        control_frame = QFrame()
        control_layout = QVBoxLayout(control_frame)

        # QTabWidget
        tab_widget = QTabWidget()
        tab_widget.addTab(SerialView(), "Serial")
        tab_widget.addTab(TCPView(), "TCP/IP")
        tab_widget.addTab(MacroView(), "Macro")

        preset_buttons_frame = PresetButtonsView("Preset 1", "Preset 2", "Preset 3", "Preset 4")
        custom_command_frame = CustomCommandView()

        # Adding widgets to the left layout
        control_layout.addWidget(tab_widget)
        control_layout.addWidget(preset_buttons_frame)
        control_layout.addWidget(custom_command_frame)

        # Center frame and layout
        feedback_frame = QFrame()
        feedback_layout = QVBoxLayout(feedback_frame)

        status_view = StatusView()
        sequence_frame = SequenceView()

        # Adding widgets to the center layout
        feedback_layout.addWidget(status_view)
        feedback_layout.addWidget(sequence_frame)

        # Log display frame
        log_display_frame = QFrame()
        log_display_layout = QVBoxLayout(log_display_frame)
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setFixedWidth(350)
        log_display_layout.addWidget(log_display)

        # Adding frames to the main layout
        main_layout.addWidget(feedback_frame)
        main_layout.addWidget(control_frame)
        main_layout.addWidget(log_display_frame)

        self.setWindowTitle("Main Window")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
