# macro_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QLineEdit

class MacroView(QWidget):

    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Macro Sequence"), 0, 0, 1, 2)
        self.macro_select_cbx = QComboBox()
        layout.addWidget(self.macro_select_cbx, 1, 0, 1, 2)

        layout.addWidget(QLabel("Total"), 0, 2, 1, 1)
        self.macro_total_cycles_lbl = QLineEdit("")
        self.macro_total_cycles_lbl.setStyleSheet("font-weight: bold; "
                                                  "background-color: #000040; "
                                                  "color: yellow; "
                                                  "qproperty-alignment: AlignCenter; ")
        layout.addWidget(self.macro_total_cycles_lbl, 1, 2, 1, 1)

        layout.addWidget(QLabel("Completed"), 0, 3, 1, 1)
        self.macro_completed_cycles_lbl = QLineEdit("")
        self.macro_completed_cycles_lbl.setStyleSheet("font-weight: bold; "
                                                      "background-color: #000040; "
                                                      "color: yellow; "
                                                      "qproperty-alignment: AlignCenter;")
        layout.addWidget(self.macro_completed_cycles_lbl, 1, 3, 1, 1)

        self.macro_start_btn = QPushButton("Start")
        self.macro_start_btn.setEnabled(False)
        layout.addWidget(self.macro_start_btn, 2, 0, 1, 2)

        self.macro_stop_btn = QPushButton("Stop")
        self.macro_stop_btn.setEnabled(True)
        layout.addWidget(self.macro_stop_btn, 2, 2, 1, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)

    def populate_macro_select_combo(self, macro_files):
        self.macro_select_cbx.clear()
        self.macro_select_cbx.addItem("")
        self.macro_select_cbx.addItems(macro_files)

    def update_total_cycles(self, cycles):
        self.macro_total_cycles_lbl.setText(str(cycles))

    def update_completed_cycles(self, cycles):
        self.macro_completed_cycles_lbl.setText(str(cycles))
        print(f"updating completed cycles {cycles}")
