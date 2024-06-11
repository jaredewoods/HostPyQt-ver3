# status_view.py

from PyQt6.QtWidgets import QWidget, QFormLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class StatusView(QWidget):
    def __init__(self):
        super().__init__()
        combined_layout = QHBoxLayout(self)

        # Form layout for status
        status_layout = QFormLayout()

        self.serial_status_label = QLabel("Inactive")
        self.serial_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serial_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_layout.addRow(QLabel("Serial:"), self.serial_status_label)

        self.tcp_status_label = QLabel("Inactive")
        self.tcp_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tcp_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_layout.addRow(QLabel("TCP:"), self.tcp_status_label)

        self.macro_status_label = QLabel("Inactive")
        self.macro_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.macro_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        status_layout.addRow(QLabel("Macro:"), self.macro_status_label)

        # Form layout for time
        time_layout = QFormLayout()

        self.start_label = QLabel("--:--:--")
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_label.setStyleSheet("padding: 5px;")
        time_layout.addRow(QLabel("Start:"), self.start_label)

        self.stop_label = QLabel("--:--:--")
        self.stop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stop_label.setStyleSheet("padding: 5px;")
        time_layout.addRow(QLabel("Stop:"), self.stop_label)

        self.run_label = QLabel("00:00:00")
        self.run_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.run_label.setStyleSheet("padding: 5px;")
        time_layout.addRow(QLabel("Run:"), self.run_label)

        # Combine status and time layouts
        combined_layout.addLayout(status_layout)
        combined_layout.addLayout(time_layout)
