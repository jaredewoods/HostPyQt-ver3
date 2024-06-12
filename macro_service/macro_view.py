# macro_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton


class MacroView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        # Macro Sequence Selection
        layout.addWidget(QLabel("Macro Sequence"), 0, 0)
        self.macro_select_combo = QComboBox()
        layout.addWidget(self.macro_select_combo, 1, 0)

        # Cycle Count Entry
        layout.addWidget(QLabel("Total Cycles"), 0, 1)
        self.macro_total_cycles_combo = QComboBox()
        layout.addWidget(self.macro_total_cycles_combo, 1, 1)

        # Macro Control Buttons
        self.macro_start_btn = QPushButton("Start")
        self.macro_start_btn.setEnabled(False)
        layout.addWidget(self.macro_start_btn, 2, 0)

        self.macro_stop_btn = QPushButton("Stop")
        self.macro_stop_btn.setEnabled(False)
        layout.addWidget(self.macro_stop_btn, 2, 1)
