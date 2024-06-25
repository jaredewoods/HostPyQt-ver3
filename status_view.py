from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class StatusView(QWidget):
    """
    Class representing a status view widget.

    This class provides a widget that displays the status of various components, such as time and connection status.

    Example usage:
        status_view = StatusView()

    Attributes:
        main_layout (QVBoxLayout): The main layout of the widget.

    Methods:
        __init__(): Initializes the StatusView widget.
        create_status_time_layout(): Creates the layout for displaying time status.
        create_status_connection_layout(): Creates the layout for displaying connection status.
        update_label_color(label, value): Updates the color of the given label based on the given value.
        update_serial_status(value): Updates the serial connection status label color based on the given value.
        update_tcp_status(value): Updates the TCP/IP connection status label color based on the given value.
        update_macro_status(value): Updates the macro status label color based on the given value.
    """
    def __init__(self):
        super().__init__()

        self.macro_status_label = None
        self.tcp_status_label = None
        self.serial_status_label = None
        self.run_label = None
        self.stop_label = None
        self.start_label = None
        self.main_layout = QVBoxLayout()

        self.create_status_time_layout()
        self.create_status_connection_layout()

        self.setLayout(self.main_layout)

    def create_status_time_layout(self):
        status_time_layout = QHBoxLayout()

        self.start_label = QLabel("--:--:--")
        status_time_layout.addWidget(QLabel("Start:"))
        status_time_layout.addWidget(self.start_label)

        self.stop_label = QLabel("--:--:--")
        status_time_layout.addWidget(QLabel("Stop:"))
        status_time_layout.addWidget(self.stop_label)

        self.run_label = QLabel("--:--:--")
        status_time_layout.addWidget(QLabel("Run"))
        status_time_layout.addWidget(self.run_label)

        self.main_layout.addLayout(status_time_layout)

    def create_status_connection_layout(self):
        status_connection_layout = QHBoxLayout()

        self.serial_status_label = QLabel("SERIAL")
        self.serial_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serial_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_connection_layout.addWidget(self.serial_status_label)

        self.tcp_status_label = QLabel(" TCP / IP ")
        self.tcp_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tcp_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_connection_layout.addWidget(self.tcp_status_label)

        self.macro_status_label = QLabel("MACRO")
        self.macro_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.macro_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_connection_layout.addWidget(self.macro_status_label)

        self.main_layout.addLayout(status_connection_layout)

    @staticmethod
    def update_label_color(label, value):
        if value:
            label.setStyleSheet("background-color: darkGreen; color: white;")
        else:
            label.setStyleSheet("background-color: darkRed; color: white;")

    def update_serial_status(self, value):
        self.update_label_color(self.serial_status_label, value)

    def update_tcp_status(self, value):
        self.update_label_color(self.tcp_status_label, value)

    def update_macro_status(self, value):
        self.update_label_color(self.macro_status_label, value)
