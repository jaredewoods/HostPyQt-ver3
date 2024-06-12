# serial_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton


class SerialView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # serial port selection
        self.serial_port_combo = QComboBox()
        layout.addWidget(QLabel("Serial Port"), 0, 0)
        layout.addWidget(self.serial_port_combo, 1, 0)

        # baud rate selection
        self.baud_combo = QComboBox()
        layout.addWidget(QLabel("Baud Rate"), 0, 1)
        layout.addWidget(self.baud_combo, 1, 1)
        self.baud_combo.addItems(["9600", "19200"])

        # serial connection buttons
        self.serial_connect_btn = QPushButton("Connect")
        self.serial_connect_btn.setEnabled(False)
        layout.addWidget(self.serial_connect_btn, 2, 0)

        self.serial_close_button = QPushButton("Close")
        self.serial_close_button.setEnabled(False)
        layout.addWidget(self.serial_close_button, 2, 1)

    def set_ports(self, ports):
        self.serial_port_combo.addItems(ports)
