# serial_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton


class SerialView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # serial port selection
        self.serial_port_cbx = QComboBox()
        layout.addWidget(QLabel("Serial Port"), 0, 0)
        layout.addWidget(self.serial_port_cbx, 1, 0)

        # baud rate selection
        self.baud_combo = QComboBox()
        layout.addWidget(QLabel("Baud Rate"), 0, 1)
        layout.addWidget(self.baud_combo, 1, 1)
        self.baud_combo.addItems(["", "9600", "19200"])

        # serial connection buttons
        self.serial_connect_btn = QPushButton("Connect")
        self.serial_connect_btn.setEnabled(False)
        layout.addWidget(self.serial_connect_btn, 2, 0)

        self.serial_close_btn = QPushButton("Close")
        self.serial_close_btn.setEnabled(False)
        layout.addWidget(self.serial_close_btn, 2, 1)

        self.serial_port_cbx.currentIndexChanged.connect(self.check_selections)
        self.baud_combo.currentIndexChanged.connect(self.check_selections)

    def check_selections(self):
        if self.serial_port_cbx.currentIndex() != -1 and self.baud_combo.currentText() != "":
            self.serial_connect_btn.setEnabled(True)
        else:
            self.serial_connect_btn.setEnabled(False)

    def set_ports(self, ports):
        self.serial_port_cbx.addItems(ports)
