from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QColor
from datetime import datetime

class StatusView(QWidget):
    def __init__(self):
        super().__init__()

        self.run_time = None
        self.stop_time = None
        self.start_time = None
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

        self.run_label = QLabel("00:00:00")
        status_time_layout.addWidget(QLabel("Run"))
        status_time_layout.addWidget(self.run_label)

        self.main_layout.addLayout(status_time_layout)

    def update_start_time(self):
        self.start_time = datetime.now().strftime("%H:%M:%S")
        self.start_label.setText(self.start_time)
    
    def update_stop_time(self):
        self.stop_time = datetime.now().strftime("%H:%M:%S")
        self.stop_label.setText(self.stop_time)
        self.update_run_time()

    def update_run_time(self):
        # TODO: this needs resolving
        # self.run_time = self.stop_time - self.start_time
        # self.run_label.setText(str(self.run_time))
        self.run_label.setText("XX-XX-XX")
    
    def create_status_connection_layout(self):
        status_connection_layout = QHBoxLayout()

        self.serial_status_label = QLabel("SERIAL")
        self.serial_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serial_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px; border: 1px solid black;")
        status_connection_layout.addWidget(self.serial_status_label)

        self.tcp_status_label = QLabel(" TCP / IP ")
        self.tcp_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tcp_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px; border: 1px solid black;")
        status_connection_layout.addWidget(self.tcp_status_label)

        self.macro_status_label = QLabel("MACRO")
        self.macro_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.macro_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px; border: 1px solid black;")
        status_connection_layout.addWidget(self.macro_status_label)

        self.main_layout.addLayout(status_connection_layout)

    @staticmethod
    def update_label_color(label, value):
        if value:
            label.setStyleSheet("background-color: darkGreen; color: white; padding: 5px; border: 1px solid black;")
        else:
            label.setStyleSheet("background-color: darkRed; color: white; padding: 5px; border: 1px solid black;")

    def update_serial_status(self, value):
        self.update_label_color(self.serial_status_label, value)

    def update_tcp_status(self, value):
        self.update_label_color(self.tcp_status_label, value)

    def update_macro_status(self, value):
        self.update_label_color(self.macro_status_label, value)

