from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton

class PresetButtonsView(QWidget):
    def __init__(self, btn_preset1_name, btn_preset2_name, btn_preset3_name, btn_preset4_name):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        self.btn_preset1 = QPushButton(btn_preset1_name)
        self.btn_preset1.setEnabled(False)
        layout.addWidget(self.btn_preset1, 4, 0)

        self.btn_preset2 = QPushButton(btn_preset2_name)
        self.btn_preset2.setEnabled(False)
        layout.addWidget(self.btn_preset2, 4, 1)

        self.btn_preset3 = QPushButton(btn_preset3_name)
        self.btn_preset3.setEnabled(False)
        layout.addWidget(self.btn_preset3, 5, 0)

        self.btn_preset4 = QPushButton(btn_preset4_name)
        self.btn_preset4.setEnabled(False)
        layout.addWidget(self.btn_preset4, 5, 1)
