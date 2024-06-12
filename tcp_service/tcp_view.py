from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton


class TCPView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # IP Address selection
        layout.addWidget(QLabel("TCP/IP Address"), 0, 0)
        self.ip_address_combo = QComboBox()
        layout.addWidget(self.ip_address_combo, 1, 0)

        # IP Port selectino
        layout.addWidget(QLabel("Port"), 0, 1)
        self.port_combo = QComboBox()
        layout.addWidget(self.port_combo, 1, 1)

        self.tcp_connect_btn = QPushButton("Connect")
        self.tcp_connect_btn.setEnabled(False)
        layout.addWidget(self.tcp_connect_btn, 2, 0)

        self.tcp_close_btn = QPushButton("Close")
        self.tcp_close_btn.setEnabled(False)
        layout.addWidget(self.tcp_close_btn, 2, 1)
