from PyQt6.QtWidgets import QWidget, QGridLayout, QCheckBox, QLineEdit, QPushButton

class CustomCommandView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        self.start_bit_checkbox = QCheckBox("Start Bit")
        self.checksum_checkbox = QCheckBox("Checksum")
        layout.addWidget(self.start_bit_checkbox, 0, 0, 1, 2)
        layout.addWidget(self.checksum_checkbox, 0, 2, 1, 2)

        self.command_line_edit = QLineEdit()
        layout.addWidget(self.command_line_edit, 1, 0, 1, 4)

        self.send_button = QPushButton("Send")
        self.clear_button = QPushButton("Clear")
        layout.addWidget(self.send_button, 2, 0, 1, 2)
        layout.addWidget(self.clear_button, 2, 2, 1, 2)
