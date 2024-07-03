from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QApplication, QMainWindow
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime


class StatusView(QWidget):
    _LABEL_WIDTH = 75  # Class variable for label width

    def __init__(self):
        super().__init__()

        self.run_time_timer = QTimer(self)
        self.run_time_timer.timeout.connect(self.update_run_time)
        self.elapsed_seconds = 0

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
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

    def create_status_time_layout(self):
        status_time_layout = QHBoxLayout()

        self.start_label = QLabel("--:--:--")
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_label.setStyleSheet("background-color: #CCCCCC; "
                                       "color: #666666; "
                                       "padding: 5px; "
                                       "border: 2px solid grey; "
                                       "border-radius: 10px;")
        self.start_label.setFixedWidth(self._LABEL_WIDTH)  # Set fixed width
        status_time_layout.addWidget(self.start_label)

        self.stop_label = QLabel("--:--:--")
        self.stop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stop_label.setStyleSheet("background-color: #CCCCCC; "
                                      "color: #666666; "
                                      "padding: 5px; "
                                      "border: 2px solid grey; "
                                      "border-radius: 10px;")
        self.stop_label.setFixedWidth(self._LABEL_WIDTH)  # Set fixed width
        status_time_layout.addWidget(self.stop_label)

        self.run_label = QLabel("00:00:00")
        self.run_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.run_label.setStyleSheet("background-color: #CCCCCC; "
                                     "color: #666666; "
                                     "padding: 5px; "
                                     "border: 2px solid grey; "
                                     "border-radius: 10px;")
        self.run_label.setFixedWidth(self._LABEL_WIDTH)  # Set fixed width
        status_time_layout.addWidget(self.run_label)

        self.main_layout.addLayout(status_time_layout)

    def create_status_connection_layout(self):
        status_connection_layout = QHBoxLayout()

        self.serial_status_label = QLabel("SERIAL")
        self.serial_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serial_status_label.setStyleSheet("background-color: #CCCCCC; "
                                               "color: #666666; "
                                               "padding: 5px; "
                                               "border: 2px solid grey; "
                                               "border-radius: 10px;")
        self.serial_status_label.setFixedWidth(self._LABEL_WIDTH)  # Set fixed width
        status_connection_layout.addWidget(self.serial_status_label)

        self.tcp_status_label = QLabel(" TCP / IP ")
        self.tcp_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tcp_status_label.setStyleSheet("background-color: #CCCCCC; "
                                            "color: #666666; "
                                            "padding: 5px; "
                                            "border: 2px solid grey; "
                                            "border-radius: 10px;")
        self.tcp_status_label.setFixedWidth(self._LABEL_WIDTH)  # Set fixed width
        status_connection_layout.addWidget(self.tcp_status_label)

        self.macro_status_label = QLabel("MACRO")
        self.macro_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.macro_status_label.setStyleSheet("background-color: #CCCCCC; "
                                              "color: #666666; "
                                              "padding: 5px; "
                                              "border: 2px solid grey; "
                                              "border-radius: 10px;")
        self.macro_status_label.setFixedWidth(self._LABEL_WIDTH)  # Set fixed width
        status_connection_layout.addWidget(self.macro_status_label)

        self.main_layout.addLayout(status_connection_layout)

    def update_start_time(self):
        self.start_label.setText(datetime.now().strftime("%H:%M:%S"))
        self.start_label.setStyleSheet("background-color: white; "
                                       "color: darkGreen; "
                                       "padding: 5px; "
                                       "border: 2px solid #002456; "
                                       "border-radius: 10px;")
        self.run_label.setStyleSheet("background-color: white; "
                                     "color: #002456; "
                                     "padding: 5px; "
                                     "border: 2px solid #002456; "
                                     "border-radius: 10px;")
        self.run_time_timer.start(1000)  # Update every second

    def update_stop_time(self):
        self.stop_label.setText(datetime.now().strftime("%H:%M:%S"))
        self.stop_label.setStyleSheet("background-color: white; "
                                      "color: #3B0000; "
                                      "padding: 5px; "
                                      "border: 2px solid #002456; "
                                      "border-radius: 10px;")
        self.run_time_timer.stop()
        self.update_run_time()

    def update_run_time(self):
        self.run_label.setStyleSheet("background-color: white; "
                                     "color: #002456; "
                                     "padding: 5px; "
                                     "border: 2px solid #002456; "
                                     "border-radius: 10px;")
        self.elapsed_seconds += 1
        hours, remainder = divmod(self.elapsed_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.run_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    @staticmethod
    def update_label_color(label, value):
        if value:
            label.setStyleSheet("background-color: lightGreen; "
                                "color: darkGreen; "
                                "padding: 5px; "
                                "border: 2px solid darkGreen; "
                                "border-radius: 10px;")
        else:
            label.setStyleSheet("background-color: #FFCCCC; "
                                "color: #3B0000; "
                                "padding: 5px; "
                                "border: 2px solid #3B0000; "
                                "border-radius: 10px;")

    def update_serial_status(self, value):
        self.update_label_color(self.serial_status_label, value)

    def update_tcp_status(self, value):
        self.update_label_color(self.tcp_status_label, value)

    def update_macro_status(self, value):
        if value:
            self.macro_status_label.setStyleSheet("background-color: white; "
                                                  "color: #002456; "
                                                  "padding: 5px; "
                                                  "border: 2px solid #002456; "
                                                  "border-radius: 10px;")
        else:
            self.macro_status_label.setStyleSheet("background-color: #FFCCCC; "
                                                  "color: #3B0000; "
                                                  "padding: 5px; "
                                                  "border: 2px solid #3B0000; "
                                                  "border-radius: 10px;")
