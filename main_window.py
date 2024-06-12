# main_window.py
from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QFrame, QTextEdit
import sys

from serial_tab import SerialView
from tcp_tab import TCPView
from macro_tab import MacroView
from status_view import StatusView
from custom_command_view import CustomCommandView

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

        custom_command_frame = CustomCommandView("Preset 1", "Preset 2", "Preset 3", "Preset 4")

        # Adding widgets to the left layout
        control_layout.addWidget(tab_widget)
        control_layout.addWidget(custom_command_frame)

        # Status view frame
        status_view = StatusView()

        # Log display frame
        log_display_frame = QFrame()
        log_display_layout = QVBoxLayout(log_display_frame)
        log_display = QTextEdit()
        log_display.setReadOnly(True)
        log_display.setFixedWidth(350)
        log_display_layout.addWidget(log_display)

        # Adding frames to the main layout
        main_layout.addWidget(control_frame)
        main_layout.addWidget(status_view)
        main_layout.addWidget(log_display_frame)

        self.setWindowTitle("Main Window")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
