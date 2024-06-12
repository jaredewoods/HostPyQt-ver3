from PyQt6.QtWidgets import QWidget, QGridLayout, QCheckBox, QLineEdit, QPushButton

class CustomCommandView(QWidget):
    def __init__(self, btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # Preset buttons
        self.btn_preset1 = QPushButton(btn_preset1_name)
        self.btn_preset1.setEnabled(False)
        layout.addWidget(self.btn_preset1, 0, 0, 1, 2)

        self.btn_preset2 = QPushButton(btn_preset2_name)
        self.btn_preset2.setEnabled(False)
        layout.addWidget(self.btn_preset2, 0, 2, 1, 2)

        self.btn_preset3 = QPushButton(btn_preset3_name)
        self.btn_preset3.setEnabled(False)
        layout.addWidget(self.btn_preset3, 1, 0, 1, 2)

        self.btn_preset4 = QPushButton(btn_preset4_name)
        self.btn_preset4.setEnabled(False)
        layout.addWidget(self.btn_preset4, 1, 2, 1, 2)

        self.command_line_edit = QLineEdit("$")
        layout.addWidget(self.command_line_edit, 2, 0, 1, 3)

        self.checksum_edit = QLineEdit()
        self.checksum_edit.setReadOnly(True)
        layout.addWidget(self.checksum_edit, 2, 3, 1, 1)

        self.send_button = QPushButton("Send")
        self.clear_button = QPushButton("Clear")
        layout.addWidget(self.send_button, 3, 0, 1, 2)
        layout.addWidget(self.clear_button, 3, 2, 1, 2)

        # Custom command widgets
        self.start_bit_checkbox = QCheckBox("Start Bit")
        self.start_bit_checkbox.setChecked(True)
        self.checksum_checkbox = QCheckBox("Checksum")
        self.checksum_checkbox.setChecked(True)
        self.carriage_return_checkbox = QCheckBox("<CR>")
        self.carriage_return_checkbox.setChecked(True)
        layout.addWidget(self.start_bit_checkbox, 4, 0, 1, 1)
        layout.addWidget(self.checksum_checkbox, 4, 1, 1, 1)
        layout.addWidget(self.carriage_return_checkbox, 4, 2, 1, 1)
