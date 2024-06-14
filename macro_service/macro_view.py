# macro_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QLineEdit

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
        self.macro_total_cycles_label = QLineEdit("")
        layout.addWidget(self.macro_total_cycles_label, 1, 1)

        # Macro Control Buttons
        self.macro_start_btn = QPushButton("Start")
        self.macro_start_btn.setEnabled(False)
        layout.addWidget(self.macro_start_btn, 2, 0)

        self.macro_stop_btn = QPushButton("Stop")
        self.macro_stop_btn.setEnabled(False)
        layout.addWidget(self.macro_stop_btn, 2, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
    def populate_macro_select_combo(self, macro_files):
        self.macro_select_combo.clear()
        self.macro_select_combo.addItem("")
        self.macro_select_combo.addItems(macro_files)

    def update_total_cycles(self, cycles):
        self.macro_total_cycles_label.setText(str(cycles))
