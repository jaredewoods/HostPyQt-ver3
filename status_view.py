from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt

class StatusView(QWidget):
    def __init__(self):
        super().__init__()

        # Create grid layout
        grid_layout = QGridLayout(self)

        # Serial status
        self.serial_status_label = QLabel("SERIAL")
        self.serial_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serial_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        grid_layout.addWidget(self.serial_status_label, 0, 0, 1, 2)

        # TCP status
        self.tcp_status_label = QLabel(" TCP ")
        self.tcp_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tcp_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        grid_layout.addWidget(self.tcp_status_label, 0, 2, 1, 2)

        # Macro status
        self.macro_status_label = QLabel("MACRO")
        self.macro_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.macro_status_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        grid_layout.addWidget(self.macro_status_label, 1, 0, 1, 2)

        # Macro status
        self.elapsed_time_label = QLabel("--:--:--")
        self.elapsed_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.elapsed_time_label.setStyleSheet("background-color: #CCCCCC; color: #666666; padding: 5px;")
        grid_layout.addWidget(self.elapsed_time_label, 1, 2, 1, 2)

        # Start time
        self.start_label = QLabel("--:--:--")
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(QLabel("Start:"), 3, 0)
        grid_layout.addWidget(self.start_label, 3, 1)

        # Stop time
        self.stop_label = QLabel("--:--:--")
        self.stop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(QLabel("Stop:"), 3, 2)
        grid_layout.addWidget(self.stop_label, 3, 3)

        # Macro sequence display
        self.sequence_display = QTextEdit()
        self.sequence_display.setReadOnly(True)
        grid_layout.addWidget(self.sequence_display, 6, 0, 1, 4)

        self.setLayout(grid_layout)
