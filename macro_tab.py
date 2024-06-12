# macro_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton


class MacroView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # Column 1
        layout.addWidget(QLabel("Macro Sequence"), 0, 0)
        layout.addWidget(QComboBox(), 1, 0)
        layout.addWidget(QPushButton("Start"), 2, 0)

        # Column 2
        layout.addWidget(QLabel("Total Cycles"), 0, 1)
        layout.addWidget(QComboBox(), 1, 1)
        layout.addWidget(QPushButton("Stop"), 2, 1)
