from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt

class StatusView(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.create_status_time_layout()
        self.create_status_connection_layout()

        self.setLayout(self.main_layout)

    def create_status_time_layout(self):
        status_time_layout = QHBoxLayout()

        self.start_label = QLabel("--:--:--")
        status_time_layout.addWidget(QLabel("Start:"))
        status_time_layout.addWidget(self.start_label)

        self.run_label = QLabel("--:--:--")
        status_time_layout.addWidget(QLabel("Run"))
        status_time_layout.addWidget(self.run_label)

        self.stop_label = QLabel("--:--:--")
        status_time_layout.addWidget(QLabel("Stop:"))
        status_time_layout.addWidget(self.stop_label)

        self.main_layout.addLayout(status_time_layout)

    def create_status_connection_layout(self):
        status_connection_layout = QHBoxLayout()

        self.serial_status_label = QLabel("SERIAL")
        self.serial_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serial_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_connection_layout.addWidget(self.serial_status_label)

        self.tcp_status_label = QLabel(" TCP ")
        self.tcp_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tcp_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_connection_layout.addWidget(self.tcp_status_label)

        self.macro_status_label = QLabel("MACRO")
        self.macro_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.macro_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_connection_layout.addWidget(self.macro_status_label)

        self.main_layout.addLayout(status_connection_layout)
