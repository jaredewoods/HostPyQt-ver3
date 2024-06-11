from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton


class TCPView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # Column 1
        layout.addWidget(QLabel("TCP/IP Address"), 0, 0)
        layout.addWidget(QComboBox(), 1, 0)
        layout.addWidget(QPushButton("Connect"), 2, 0)

        # Column 2
        layout.addWidget(QLabel("Port"), 0, 1)
        layout.addWidget(QComboBox(), 1, 1)
        layout.addWidget(QPushButton("Close"), 2, 1)
